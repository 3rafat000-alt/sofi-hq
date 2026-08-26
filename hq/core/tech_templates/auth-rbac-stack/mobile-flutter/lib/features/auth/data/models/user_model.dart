/// نماذج المستخدم وفق UserPayload/RolePayload في العقد حرفياً.
///
/// العقد الحاكم: docs/openapi-auth.md → components.schemas.UserPayload
///
/// قواعد الغرفة: **ممنوع mock يدوي** — كل حقول وأسماء المفاتيح من العقد حصراً:
/// {id, name, email, status, created_at, role{id,name,display_name}, permissions[]}
/// - `role` قابل لأن يكون null (RolePayload nullable في العقد).
/// - `permissions` مصفوفة أسماء آلية مسطحة (مثل users.create) — strings فقط.
library;

/// الدور كما يرسله الخادم: {id, name, display_name}
class RoleModel {
  const RoleModel({
    required this.id,
    required this.name,
    required this.displayName,
  });

  final int id;
  final String name;
  final String displayName;

  factory RoleModel.fromJson(Map<String, dynamic> json) => RoleModel(
        id: json['id'] as int,
        name: json['name'] as String,
        displayName: json['display_name'] as String,
      );
}

/// المستخدم كما يرسله الخادم في data.user لكل من register/login/me.
class UserModel {
  const UserModel({
    required this.id,
    required this.name,
    required this.email,
    required this.status,
    required this.createdAt,
    required this.role,
    required this.permissions,
  });

  final int id;
  final String name;
  final String email;

  /// active | suspended | banned — enum نصي في العقد.
  final String status;
  final String createdAt; // ISO-8601 — نبقيه نصاً بلا اعتماديات إضافية.

  /// nullable وفق RolePayload (nullable: true).
  final RoleModel? role;
  final List<String> permissions;

  factory UserModel.fromJson(Map<String, dynamic> json) => UserModel(
        id: json['id'] as int,
        name: json['name'] as String,
        email: json['email'] as String,
        status: json['status'] as String,
        createdAt: json['created_at'] as String,
        // Eager parsing: الدور والصلاحيات يُفكَّكان هنا مباشرة عند أول استلام
        // (register/login/me) — جاهزان للبوابة الواجهية دون نداءات لاحقة.
        role: json['role'] == null
            ? null
            : RoleModel.fromJson(json['role'] as Map<String, dynamic>),
        permissions: (json['permissions'] as List<Object?>? ?? const [])
            .whereType<String>()
            .toList(),
      );
}
