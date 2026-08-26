/// مستودع المصادقة — العمود الفاصل بين الشبكة والحالة.
///
/// يستدعي ApiClient حصراً (لا http مباشر هنا) ويحوّل data إلى نماذج العقد:
/// - register/login → AuthData {user, token, token_type}  (201/200)
/// - me             → MeData {user}                        (200)
/// - logout         → MessageData {message_ar, message_en}  (200)
///
/// أي فشل يصل هنا كمغلف v1 مرفوعاً مسبقاً كـ AuthException من api_client
/// برموز العقد الثابتة ورسائلها العربية الجاهزة للعرض.
library;

import '../../../../core/network/api_client.dart';
import '../models/user_model.dart';

/// نتيجة نجاح المصادقة: المستخدم + التوكن معاً (AuthData في العقد).
class AuthResult {
  const AuthResult({required this.user, required this.token});

  final UserModel user;
  final String token;
}

class AuthRepository {
  AuthRepository(this._client);

  final ApiClient _client;

  /// POST /register — الحقول بأسماء العقد: name, email,
  /// password, password_confirmation. يعيد توكن فوري (دخول تلقائي).
  Future<AuthResult> register({
    required String name,
    required String email,
    required String password,
    required String passwordConfirmation,
  }) =>
      _authenticate(ApiClient.registerPath, {
        'name': name,
        'email': email,
        'password': password,
        'password_confirmation': passwordConfirmation,
      });

  /// POST /login — {email, password}.
  Future<AuthResult> login({
    required String email,
    required String password,
  }) =>
      _authenticate(ApiClient.loginPath, {
        'email': email,
        'password': password,
      });

  /// GET /me — هوية المستخدم الحالية مع role + permissions (Eager Loaded).
  Future<UserModel> me() => _client.get<Object?>(
        ApiClient.mePath,
        parse: (raw) =>
            UserModel.fromJson(_requireMap(raw)['user'] as Map<String, dynamic>),
      );

  /// POST /logout — يسحب التوكن الحالي فقط؛ النجاح رسالة لا نحتاج عرضها.
  Future<void> logout() =>
      _client.post<Object?>(ApiClient.logoutPath, parse: (_) => null);

  /// تفكيك AuthData الموحد لـ register/login — Eager parsing للمستخدم
  /// (role + permissions داخل UserModel.fromJson) والتوكن معاً.
  Future<AuthResult> _authenticate(
    String path,
    Map<String, Object?> body,
  ) =>
      _client.post<AuthResult>(
        path,
        body: body,
        parse: (raw) {
          final data = _requireMap(raw);
          return AuthResult(
            user: UserModel.fromJson(data['user'] as Map<String, dynamic>),
            token: data['token'] as String,
          );
        },
      );

  static Map<String, dynamic> _requireMap(Object? raw) {
    if (raw is! Map<String, dynamic>) {
      // مغلف ناجح لكن data بنيته غير مطابقة للعقد — عطل تكوين خادم.
      throw const AuthException(
        code: 'SERVER_ERROR',
        messageAr: 'استجابة غير متوقعة من الخادم.',
      );
    }
    return raw;
  }
}
