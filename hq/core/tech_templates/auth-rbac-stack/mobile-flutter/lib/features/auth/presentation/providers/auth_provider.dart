/// ════════════════════════════════════════════════════════════════════════
/// قرار إدارة الحالة: ChangeNotifier + provider (وليس BLoC)
/// ────────────────────────────────────────────────────────────────────────
/// السبب، موثقاً كما طلب أمر العمل RCCF:
/// 1. قالب مرجعي تعليمي — Provider بلا codegen ولا طبقة أحداث إضافية،
///    فيقرأه القادم الجديد في دقائق (state واحد صريح بدل Cubit/State pairs).
/// 2. نطاق الميزة صغير ومتسلسل (نموذجان + 4 نداءات) — BLoC قوته في تدفقات
///    معقدة متعددة الأحداث، وهنا overhead بلا مقابل.
/// 3. نفس نمط Envelope<T>/Repository يعمل فوق أي حل حالة — الترقية إلى BLoC
///    لاحقة لا تلمس إلا هذا الملف والشاشات.
/// ════════════════════════════════════════════════════════════════════════
///
/// حالة المصادقة الموحدة: idle/loading/success/error مع رسالة عربية جاهزة
/// للعرض من `messageAr` في العقد، وأخطاء الحقول من `error.fields`.
///
/// ملزم من العقد (الملاحظة 4): عند code == UNAUTHENTICATED نظّف الجلسة
/// فوراً — منفذ في [_handleFailure].
library;

import 'package:flutter/foundation.dart';

import '../../../../core/network/api_client.dart';
import '../../../../core/storage/token_storage.dart';
import '../../data/models/user_model.dart';
import '../../data/repositories/auth_repository.dart';

enum AuthStatus { idle, loading, success, error }

class AuthProvider extends ChangeNotifier {
  AuthProvider(this._repo, this._storage);

  final AuthRepository _repo;
  final TokenStorage _storage;

  AuthStatus _status = AuthStatus.idle;
  UserModel? _user;
  String? _token;
  String? _errorAr;
  Map<String, List<String>>? _fieldErrors;
  bool _busy = false; // درع إعادة الدخول: لا نداءان متوازيان.

  AuthStatus get status => _status;
  bool get isLoading => _status == AuthStatus.loading;
  UserModel? get user => _user;
  String? get token => _token;

  /// الرسالة العربية المعروضة عند error — جاهزة من messageAr بالعقد.
  String? get errorAr => _errorAr;

  /// أخطاء الحقول من error.fields — null إلا في VALIDATION_FAILED.
  Map<String, List<String>>? get fieldErrors => _fieldErrors;

  bool get isAuthenticated => _token != null && _user != null;

  /// تسجيل حساب جديد — يعيد true عند النجاح (دخول تلقائي بتوكن فوري).
  Future<bool> register({
    required String name,
    required String email,
    required String password,
    required String passwordConfirmation,
  }) async =>
      _run(() => _repo.register(
            name: name,
            email: email,
            password: password,
            passwordConfirmation: passwordConfirmation,
          ));

  /// تسجيل الدخول — يعيد true عند النجاح.
  Future<bool> login({
    required String email,
    required String password,
  }) async =>
      _run(() => _repo.login(email: email, password: password));

  /// استرجاع الجلسة عند الإقلاع: توكن محفوظ؟ → تحقق به عبر /me واملأ المستخدم.
  /// يقرر main.dart المسار الأولي بناء على الناتج.
  Future<bool> restoreSession() async {
    final saved = await _storage.read();
    if (saved == null || saved.isEmpty) return false;
    return _run(() async {
      final user = await _repo.me(); // يرفع UNAUTHENTICATED لو التوكن انتهى.
      return AuthResult(user: user, token: saved);
    });
  }

  /// تسجيل الخروج: نسحب التوكن لدى الخادم ثم نمسح الجلسة محلياً مهما حدث.
  Future<void> logout() async {
    try {
      await _repo.logout();
    } on AuthException {
      // حتى لو فشل النداء (توكن انتهى/انقطاع) — الجلسة المحلية تُمسح دائماً.
    } finally {
      await _clearSession(notify: false);
      _status = AuthStatus.idle;
      notifyListeners();
    }
  }

  /// المنفّذ الموحد: loading ← نداء ← success/error، مع حفظ/تنظيف التوكن.
  Future<bool> _run(Future<AuthResult> Function() action) async {
    if (_busy) return false;
    _busy = true;
    _status = AuthStatus.loading;
    _errorAr = null;
    _fieldErrors = null;
    notifyListeners();

    try {
      final result = await action();
      _user = result.user;
      _token = result.token;
      await _storage.save(result.token);
      _status = AuthStatus.success;
      return true;
    } on AuthException catch (e) {
      _status = AuthStatus.error;
      await _handleFailure(e);
      return false;
    } finally {
      _busy = false;
      notifyListeners();
    }
  }

  Future<void> _handleFailure(AuthException e) async {
    _errorAr = e.messageAr;
    _fieldErrors = e.fields;
    // ملاحظة العقد الملزمة رقم 4: UNAUTHENTICATED ⇒ تنظيف الجلسة وإعادة التوجيه.
    if (e.code == 'UNAUTHENTICATED') {
      await _clearSession(notify: false);
    }
  }

  Future<void> _clearSession({bool notify = true}) async {
    _user = null;
    _token = null;
    await _storage.clear();
    if (notify) notifyListeners();
  }
}
