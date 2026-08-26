/// تخزين توكن الجلسة — تجريد بسيط فوق SharedPreferences.
///
/// التصميم:
/// - [SessionStore] يحتفظ بنسخة ذاكرة من التوكن لقراءة **متزامنة** عند بناء
///   ترويسة Authorization في كل نداء (ApiClient لا يستطيع انتظار Future).
/// - الكتابة/الحذف تُمرَّر فوراً إلى SharedPreferences للبقاء بين التشغيلات.
/// - الواجهة [TokenStorage] معزولة لتسهيل الاستبدال بـ secure storage مستقبلاً
///   دون لمس طبقات عليا.
library;

import 'package:shared_preferences/shared_preferences.dart';

/// عقد التخزين — حفظ/قراءة/مسح التوكن فقط.
abstract class TokenStorage {
  Future<void> save(String token);
  Future<String?> read();
  Future<void> clear();
}

/// التنفيذ الفعلي: SharedPreferences + نسخة ذاكرة متزامنة.
class SessionStore implements TokenStorage {
  SessionStore(this._prefs) : _cached = _prefs.getString(_storageKey);

  static const String _storageKey = 'auth.token';

  final SharedPreferences _prefs;
  String? _cached;

  /// قراءة متزامنة من الذاكرة — مخصصة لـ ApiClient عند كل طلب.
  String? get cachedToken => _cached;

  @override
  Future<void> save(String token) async {
    _cached = token;
    await _prefs.setString(_storageKey, token);
  }

  @override
  Future<String?> read() async {
    _cached ??= _prefs.getString(_storageKey);
    return _cached;
  }

  @override
  Future<void> clear() async {
    _cached = null;
    await _prefs.remove(_storageKey);
  }
}
