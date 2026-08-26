/// عمود الشبكة الفقري الوحيد للتطبيق — كل نداء HTTP يمر من هنا حصراً
/// (معيار STACKS.md: «نقطة شبكة واحدة لكل عميل»).
///
/// المسؤوليات:
/// - إرسال post/get نحو `/api/v1` مع ترويسة `Authorization: Bearer` تلقائياً عند توفر توكن.
/// - تفكيك مغلف Envelope v1 مركزياً (نموذج واحد: core/models/envelope.dart).
/// - رفع [AuthException] عند أي فشل — تحمل {code, messageAr, fields} من العقد حرفياً.
///
/// رموز الأخطاء تأتي حصراً من العقد عندما يصل مغلف من الخادم. رمزان عميليان فقط
/// (NETWORK_ERROR / SERVER_ERROR بدون مغلف) يُستخدمان حين لا يوجد مغلف أصلاً
/// (انقطاع اتصال / استجابة غير JSON) — موثق هنا لأن العقد لا يغطي انعدام الاتصال.
library;

import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/envelope.dart';

/// استثناء المصادقة/الشبكة الموحد — الطبقات العليا تلتقطه وتعرض messageAr.
class AuthException implements Exception {
  const AuthException({
    required this.code,
    required this.messageAr,
    this.fields,
  });

  /// من جسم خطأ العقد كما هو — بلا أي إعادة صياغة.
  factory AuthException.fromError(ApiError error) => AuthException(
        code: error.code,
        messageAr: error.messageAr,
        fields: error.fields,
      );

  /// لا يوجد اتصال بالخادم أو انتهت المهلة — لا مغلف في هذه الحالة أصلاً.
  factory AuthException.network() => const AuthException(
        code: 'NETWORK_ERROR',
        messageAr: 'تعذر الاتصال بالخادم، تحقق من اتصالك بالإنترنت.',
      );

  /// استجابة وصلت لكنها ليست مغلف v1 صالحاً (JSON مكسور/HTML خطأ خادم).
  factory AuthException.malformed() => const AuthException(
        code: 'SERVER_ERROR',
        messageAr: 'استجابة غير متوقعة من الخادم.',
      );

  final String code;
  final String messageAr;
  final Map<String, List<String>>? fields;

  @override
  String toString() => 'AuthException($code): $messageAr';
}

/// عميل الـHTTP الموحد.
class ApiClient {
  ApiClient({
    required this.baseUrl,
    http.Client? client,
    String? Function()? tokenProvider,
    this.timeout = const Duration(seconds: 20),
  })  : _client = client ?? http.Client(),
        _tokenProvider = tokenProvider;

  /// مثال: http://10.0.2.2:8000/api/v1 — يُمرَّر عبر --dart-define في الإنتاج.
  final String baseUrl;
  final http.Client _client;
  final String? Function()? _tokenProvider;
  final Duration timeout;

  // مسارات عقد المصادقة — مصدرها docs/openapi-auth.md#خلاصة-سريعة.
  static const String registerPath = '/register';
  static const String loginPath = '/login';
  static const String logoutPath = '/logout';
  static const String mePath = '/me';

  /// POST مع تفكيك المغلف وإعادة data محولة إلى T.
  Future<T> post<T>(
    String path, {
    Map<String, Object?>? body,
    required T Function(Object? raw) parse,
  }) =>
      _send<T>('POST', path, body, parse);

  /// GET مع تفكيك المغلف وإعادة data محولة إلى T.
  Future<T> get<T>(
    String path, {
    required T Function(Object? raw) parse,
  }) =>
      _send<T>('GET', path, null, parse);

  Future<T> _send<T>(
    String method,
    String path,
    Map<String, Object?>? body,
    T Function(Object? raw) parse,
  ) async {
    final uri = Uri.parse('$baseUrl$path');
    final token = _tokenProvider?.call();
    final headers = <String, String>{
      'Accept': 'application/json',
      if (body != null) 'Content-Type': 'application/json',
      if (token != null && token.isNotEmpty) 'Authorization': 'Bearer $token',
    };

    http.Response response;
    try {
      response = method == 'GET'
          ? await _client.get(uri, headers: headers).timeout(timeout)
          : await _client
              .post(uri, headers: headers,
                  body: body == null ? null : jsonEncode(body))
              .timeout(timeout);
    } on TimeoutException {
      throw AuthException.network();
    } on Exception {
      // SocketException/ClientException وغيرها — كلها «لا اتصال فعلي» من منظور الواجهة.
      throw AuthException.network();
    }

    final Map<String, dynamic> decoded;
    try {
      final raw = jsonDecode(utf8.decode(response.bodyBytes));
      if (raw is! Map<String, dynamic>) throw const FormatException();
      decoded = raw;
    } on FormatException {
      throw AuthException.malformed();
    }

    // تفكيك مركزي للمغلف — الجذور الأربعة كما هي من العقد.
    final envelope =
        Envelope<Object?>.fromJson(decoded, dataConverter: (raw) => raw);

    if (!envelope.success || envelope.error != null) {
      throw AuthException.fromError(
        envelope.error ??
            const ApiError(
              code: 'SERVER_ERROR',
              messageAr: 'حدث خطأ غير متوقع.',
              messageEn: 'Unexpected error.',
              fields: null,
            ),
      );
    }

    return parse(envelope.data);
  }

  void close() => _client.close();
}
