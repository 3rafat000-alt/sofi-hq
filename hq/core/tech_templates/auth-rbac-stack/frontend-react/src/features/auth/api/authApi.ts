/**
 * العمود الفقري لنداءات المصادقة — الطبقة الوحيدة التي ترى JSON الخام في هذه الميزة.
 *
 * الالتزامات المنفذة هنا (hq/core/API-ENVELOPE.md — التزامات غرفة الفرونت إند):
 *   1. تفكيك المغلف v1 يتم هنا مرة واحدة — المكوّنات والhooks تستقبل بيانات مجرّدة.
 *   2. error.code يقود السلوك: UNAUTHENTICATED ينظّف الجلسة فوراً (ملاحظة ملزمة 4 في العقد).
 *   3. لا mock ولا أشكال JSON مفترضة — الأشكال من types.ts المشتق من OpenAPI حصراً.
 *
 * الأخطاء تُرمى موحّدة: AuthApiError { code, messageAr, fields } —
 * messageAr جاهزة للعرض العربي (من error.message_ar حرفياً) وfields لأخطاء الحقول.
 */
import type {
  AssignRolePayload,
  AuthData,
  ErrorCode,
  LoginPayload,
  MeData,
  MessageData,
  RegisterPayload,
  RoleName,
  User,
} from '../types';

/* ────────────────────────────────────────────────────────────────
 * الإعداد والتوكن
 * ──────────────────────────────────────────────────────────────── */

/** عنوان الـAPI الافتراضي — قابل للتجاوز عبر VITE_API_BASE_URL عند الدمج */
function readBaseUrl(): string {
  try {
    const env = (import.meta as { env?: Record<string, string | undefined> }).env;
    return env?.VITE_API_BASE_URL ?? '/api/v1';
  } catch {
    return '/api/v1';
  }
}

const BASE_URL: string = readBaseUrl();

/** مفتاح توكن موحّد — المصدر الوحيد لحالة الجلسة في المتصفح */
export const TOKEN_STORAGE_KEY = 'auth.token';

/** قراءة التوكن — null يعني لا جلسة */
export function getToken(): string | null {
  try {
    return window.localStorage.getItem(TOKEN_STORAGE_KEY);
  } catch {
    return null;
  }
}

/** حفظ التوكن بعد login/register ناجح */
export function setToken(token: string): void {
  try {
    window.localStorage.setItem(TOKEN_STORAGE_KEY, token);
  } catch {
    /* التخزين غير متاح (وضع خاص/حصة ممتلئة) — الجلسة لن تدوم لكن النداء الحالي ينجح */
  }
}

/** مسح التوكن — يُستدعى آلياً عند UNAUTHENTICATED وعند logout */
export function clearToken(): void {
  try {
    window.localStorage.removeItem(TOKEN_STORAGE_KEY);
  } catch {
    /* التخزين غير متاح — لا شيء لمسحه */
  }
}

/* ────────────────────────────────────────────────────────────────
 * خطأ المصادقة الموحّد
 * ──────────────────────────────────────────────────────────────── */

/**
 * خطأ المصادقة الموحّد — ما ترميه هذه الطبقة حصراً.
 * messageAr جاهزة للعرض العربي (منسوخة من error.message_ar في المغلف)،
 * وfields لأخطاء الحقول العربية (null إلا في VALIDATION_FAILED).
 */
export class AuthApiError extends Error {
  public readonly code: ErrorCode;
  /** رسالة عربية جاهزة للعرض — من error.message_ar حرفياً */
  public readonly messageAr: string;
  /** أخطاء الحقول العربية — null إلا في VALIDATION_FAILED */
  public readonly fields: Record<string, string[]> | null;

  constructor(
    code: ErrorCode,
    messageAr: string,
    fields: Record<string, string[]> | null = null,
    options?: ErrorOptions,
  ) {
    super(messageAr, options);
    this.name = 'AuthApiError';
    this.code = code;
    this.messageAr = messageAr;
    this.fields = fields;
    Object.setPrototypeOf(this, AuthApiError.prototype);
  }
}

/* ────────────────────────────────────────────────────────────────
 * تفكيك المغلف v1 — المكان الوحيد الذي يلمس JSON الخام
 * ──────────────────────────────────────────────────────────────── */

const ERROR_CODES: readonly ErrorCode[] = [
  'VALIDATION_FAILED',
  'UNAUTHENTICATED',
  'FORBIDDEN',
  'NOT_FOUND',
  'CONFLICT',
  'RATE_LIMITED',
  'SERVER_ERROR',
];

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

/** تطبيق حقول أخطاء الحقول — يتجاهل أي شكل لا يطابق Record<string, string[]> */
function extractFields(value: unknown): Record<string, string[]> | null {
  if (typeof value !== 'object' || value === null) return null;
  const out: Record<string, string[]> = {};
  for (const [key, messages] of Object.entries(value)) {
    if (Array.isArray(messages) && messages.every((m) => typeof m === 'string')) {
      out[key] = messages;
    }
  }
  return Object.keys(out).length > 0 ? out : null;
}

/**
 * تفكيك المغلف v1 — المكان الوحيد في الميزة التي يلمس JSON الخام.
 * يرجع data عند النجاح، ويرمي AuthApiError عند الفشل مع تطبيق ملاحظة العقد الملزمة 4
 * (UNAUTHENTICATED ⇒ مسح الجلسة فوراً).
 */
async function unwrapEnvelope(response: Response): Promise<unknown> {
  let body: unknown;
  try {
    body = await response.json();
  } catch {
    throw new AuthApiError('SERVER_ERROR', 'تعذّرت قراءة استجابة الخادم.');
  }

  if (typeof body !== 'object' || body === null) {
    throw new AuthApiError('SERVER_ERROR', 'استجابة غير متوقعة من الخادم.');
  }

  const envelope = body as Record<string, unknown>;
  if (typeof envelope.success !== 'boolean') {
    throw new AuthApiError('SERVER_ERROR', 'استجابة غير متوقعة من الخادم.');
  }

  if (envelope.success === false) {
    const rawError: unknown = envelope.error;
    if (
      typeof rawError === 'object' &&
      rawError !== null &&
      typeof (rawError as Record<string, unknown>).code === 'string' &&
      typeof (rawError as Record<string, unknown>).message_ar === 'string'
    ) {
      const err = rawError as Record<string, unknown>;
      const rawCode = err.code;
      const isValidCode = typeof rawCode === 'string' &&
        (ERROR_CODES as readonly string[]).includes(rawCode);
      if (isValidCode) {
        const code = rawCode as ErrorCode;
        // ملاحظة العقد الملزمة 4: عند UNAUTHENTICATED نظّف الجلسة فوراً
        if (code === 'UNAUTHENTICATED') clearToken();
        throw new AuthApiError(
          code,
          err.message_ar as string,
          extractFields(err.fields),
        );
      }
    }
    throw new AuthApiError('SERVER_ERROR', 'استجابة غير متوقعة من الخادم.');
  }

  return envelope.data;
}

/* ────────────────────────────────────────────────────────────────
 * نواة الطلب + endpoints العقد الخمسة
 * ──────────────────────────────────────────────────────────────── */

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT';
  body?: unknown;
  signal?: AbortSignal;
}

/** نواة الطلب المشتركة — بناء الترويسات + Bearer تلقائياً عند وجود توكن */
async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const headers: Record<string, string> = { Accept: 'application/json' };
  if (options.body !== undefined) headers['Content-Type'] = 'application/json';

  const token = getToken();
  if (token !== null) headers.Authorization = `Bearer ${token}`;

  let response: Response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method: options.method ?? 'GET',
      headers,
      body: options.body === undefined ? null : JSON.stringify(options.body),
      signal: options.signal,
    });
  } catch (cause) {
    throw new AuthApiError('SERVER_ERROR', 'تعذّر الاتصال بالخادم. تحقق من اتصالك.', null, {
      cause,
    });
  }

  return unwrapEnvelope(response) as Promise<T>;
}

/** POST /register — 201 EnvelopeAuth (throttle: 10/دقيقة ⇒ RATE_LIMITED محتمل) */
export function register(payload: RegisterPayload): Promise<AuthData> {
  return request<AuthData>('/register', { method: 'POST', body: payload });
}

/** POST /login — 200 EnvelopeAuth | 401 بيانات خاطئة | 403 موقوف/محظور | 429 */
export function login(payload: LoginPayload): Promise<AuthData> {
  return request<AuthData>('/login', { method: 'POST', body: payload });
}

/** POST /logout — 200 EnvelopeMessage | 401 (يتطلب Bearer) */
export function logout(options: { signal?: AbortSignal } = {}): Promise<MessageData> {
  return request<MessageData>('/logout', { method: 'POST', signal: options.signal });
}

/** GET /me — 200 EnvelopeMe | 401 — يرجع User مباشرة (تفكيك data.user هنا) */
export async function me(options: { signal?: AbortSignal } = {}): Promise<User> {
  const data: MeData = await request<MeData>('/me', { signal: options.signal });
  return data.user;
}

/** PUT /users/{user}/role — 200 EnvelopeMe | 403 escalation guard | 404 | 422 */
export async function assignRole(
  userId: number,
  payload: AssignRolePayload,
  options: { signal?: AbortSignal } = {},
): Promise<User> {
  const data = await request<{ user: User }>(`/users/${userId}/role`, {
    method: 'PUT',
    body: payload,
    signal: options.signal,
  });
  return data.user;
}
