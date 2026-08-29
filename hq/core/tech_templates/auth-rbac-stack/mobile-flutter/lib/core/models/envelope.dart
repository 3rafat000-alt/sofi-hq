/// Envelope v1 — المغلف الموحد لكل استجابات الـAPI (عقد المصادقة الرسمي).
///
/// المصدر الحاكم: `templates/auth-rbac-stack/backend-laravel/docs/openapi-auth.md`
/// (المطابق حرفياً لـ `hq/core/API-ENVELOPE.md#envelope-v1`).
///
/// قواعد ملزمة من العقد:
/// 1. الجذور الأربعة ثابتة دائماً: success | data | error | meta — لا حذف ولا إضافة.
/// 2. عند النجاح: error = null و data غير فارغ. عند الفشل: data = null و error غير فارغ.
/// 3. `error.fields` = null إلا في VALIDATION_FAILED، ورسائلها عربية تفصيلية.
///
/// هذا هو نموذج المغلف **الوحيد** في طبقة البيانات — parsing مركزي، لا تفكيك يدوي
/// للاستجابات في أي مكان آخر (قاعدة غرفة الموبايل: ممنوع mock يدوي أو parsing متناثر).
library;

/// بيانات الـmeta الثابتة في كل استجابة.
class Meta {
  const Meta({required this.timestamp, required this.apiVersion});

  final String timestamp;
  final String apiVersion;

  factory Meta.fromJson(Map<String, dynamic> json) => Meta(
        timestamp: json['timestamp'] as String? ?? '',
        apiVersion: json['api_version'] as String? ?? 'v1',
      );
}

/// جسم الخطأ القياسي وفق ErrorBody في العقد:
/// {code, message_ar, message_en, fields}
class ApiError {
  const ApiError({
    required this.code,
    required this.messageAr,
    required this.messageEn,
    required this.fields,
  });

  /// رمز ثابت من العقد: VALIDATION_FAILED | UNAUTHENTICATED | FORBIDDEN |
  /// NOT_FOUND | CONFLICT | RATE_LIMITED | SERVER_ERROR
  final String code;

  /// الرسالة العربية المعروضة للمستخدم مباشرة.
  final String messageAr;
  final String messageEn;

  /// خريطة الحقل → رسائله العربية؛ null إلا في VALIDATION_FAILED.
  final Map<String, List<String>>? fields;

  factory ApiError.fromJson(Map<String, dynamic> json) => ApiError(
        code: json['code'] as String? ?? 'SERVER_ERROR',
        messageAr: json['message_ar'] as String? ?? 'حدث خطأ غير متوقع.',
        messageEn: json['message_en'] as String? ?? 'Unexpected error.',
        fields: _parseFields(json['fields']),
      );

  static Map<String, List<String>>? _parseFields(Object? raw) {
    if (raw is! Map<String, dynamic>) return null; // null أو شكل غير متوقع
    return raw.map(
      (field, messages) => MapEntry(
        field,
        (messages as List<Object?>).whereType<String>().toList(),
      ),
    );
  }
}

/// المغلف العام Envelope<T> — T نوع حقل data بعد التحويل.
class Envelope<T> {
  const Envelope({
    required this.success,
    required this.data,
    required this.error,
    required this.meta,
  });

  final bool success;
  final T? data;
  final ApiError? error;
  final Meta meta;

  /// Parsing مركزي وحيد: يقرأ الجذور الأربعة ويحوّل data عبر [dataConverter]
  /// الذي تمرره طبقة المستودع بحسب نوع الاستجابة (AuthData / MeData / MessageData).
  factory Envelope.fromJson(
    Map<String, dynamic> json, {
    T Function(Object? raw)? dataConverter,
  }) {
    return Envelope<T>(
      success: json['success'] == true,
      data: json.containsKey('data')
          ? dataConverter?.call(json['data'])
          : null,
      error: json['error'] is Map<String, dynamic>
          ? ApiError.fromJson(json['error'] as Map<String, dynamic>)
          : null,
      meta: json['meta'] is Map<String, dynamic>
          ? Meta.fromJson(json['meta'] as Map<String, dynamic>)
          : const Meta(timestamp: '', apiVersion: 'v1'),
    );
  }
}
