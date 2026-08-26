/**
 * أنواع المصادقة — منشأة من العقد حصراً (قاعدة "لا mock يدوي"):
 *   - المصدر الأول: templates/auth-rbac-stack/backend-laravel/docs/openapi-auth.md (OpenAPI 3.1)
 *   - المصدر الثاني: hq/core/API-ENVELOPE.md (المغلف v1)
 * أي تغيير في الأشكال يبدأ من العقد ثم يُحدَّث هنا — لا تخمين لأشكال JSON.
 */

/* ────────────────────────────────────────────────────────────────
 * Schemas من components.schemas في openapi-auth.md
 * ──────────────────────────────────────────────────────────────── */

/** RolePayload.name — enum مثبتة في العقد */
export type RoleName = 'super-admin' | 'manager' | 'user';

/** UserPayload.status — enum مثبتة في العقد */
export type UserStatus = 'active' | 'suspended' | 'banned';

/** RolePayload — nullable عند وروده ضمن UserPayload.role */
export interface Role {
  id: number;
  name: RoleName;
  display_name: string;
}

/** UserPayload — الإسقاط الرسمي للمستخدم (لا نموذج Eloquent خاماً) */
export interface User {
  id: number;
  name: string;
  email: string;
  status: UserStatus;
  /** ISO 8601 date-time */
  created_at: string;
  role: Role | null;
  /** أسماء آلية مسطّحة مثل users.create — لبوابات الواجهة مباشرة (ملاحظة ملزمة 3 في العقد) */
  permissions: string[];
}

/** AuthData — data الخاصة بـ login/register الناجحين (200/201) */
export interface AuthData {
  user: User;
  /** Sanctum plaintext token — يُرسل لاحقاً في ترويسة Authorization: Bearer */
  token: string;
  /** const "Bearer" في العقد */
  token_type: 'Bearer';
}

/** MeData — data الخاصة بـ GET /me */
export interface MeData {
  user: User;
}

/** MessageData — data الخاصة بـ logout الناجح */
export interface MessageData {
  message_ar: string;
  message_en: string;
}

/** Meta — تذييل المغلف (required: timestamp, api_version) */
export interface Meta {
  timestamp: string;
  api_version: 'v1';
}

/* ────────────────────────────────────────────────────────────────
 * المغلف v1 — hq/core/API-ENVELOPE.md
 * ──────────────────────────────────────────────────────────────── */

/** رموز الأخطاء الثابتة — ErrorBody.code في العقد */
export type ErrorCode =
  | 'VALIDATION_FAILED'
  | 'UNAUTHENTICATED'
  | 'FORBIDDEN'
  | 'NOT_FOUND'
  | 'CONFLICT'
  | 'RATE_LIMITED'
  | 'SERVER_ERROR';

/** ErrorBody من العقد — fields=null إلا في VALIDATION_FAILED، ورسائلها عربية تفصيلية */
export interface ApiError {
  code: ErrorCode;
  message_ar: string;
  message_en: string;
  fields: Record<string, string[]> | null;
}

/** المغلف v1 — نجاح (success: true ثابتة) */
export interface Envelope<T> {
  success: true;
  data: T;
  error: null;
  meta: Meta;
}

/** المغلف v1 — فشل (success: false ثابتة) */
export interface EnvelopeError {
  success: false;
  data: null;
  error: ApiError;
  meta: Meta;
}

/** كل استجابة ممكنة من الخادم — لا شكل رابع مسموح (ملاحظة ملزمة 1 في العقد) */
export type ApiResponse<T> = Envelope<T> | EnvelopeError;

/* ────────────────────────────────────────────────────────────────
 * أسماء مستعارة من العقد + أجسام الطلب (paths في OpenAPI)
 * ──────────────────────────────────────────────────────────────── */

/** استجابة login/register الناجحة (= AuthData في العقد) */
export type AuthResponse = AuthData;

/** POST /login — requestBody في العقد */
export interface LoginPayload {
  email: string;
  password: string;
}

/** POST /register — requestBody في العقد */
export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
  password_confirmation: string;
}

/** PUT /users/{user}/role — requestBody في العقد */
export interface AssignRolePayload {
  role: RoleName;
}
