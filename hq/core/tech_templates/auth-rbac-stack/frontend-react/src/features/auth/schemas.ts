/**
 * مخططات Zod للنماذج — مطابقة حرفياً لقيود FormRequests الخلفية:
 *   - templates/auth-rbac-stack/backend-laravel/app/Http/Requests/RegisterRequest.php
 *   - templates/auth-rbac-stack/backend-laravel/app/Http/Requests/LoginRequest.php
 * الرسائل العربية أدناه منسوخة حرفياً من messages() في كل FormRequest
 * (مع تعويض :max/:min بقيديهما 255/8 كما يفعل Laravel).
 *
 * قرار موثّق حول قاعدة `lowercase`:
 *   هي قاعدة رفض في Laravel (لا تحويل) — AuthController يبحث بالبريد كما ورد.
 *   لذلك نطبّع البريد قبل الإرسال (trim + lowercase) عبر normalizeEmail() في onSubmit،
 *   فلا يصل بريد بأحرف كبيرة للخادم أصلاً — مطابق لوصف العقد "Lowercased"
 *   وبلا عقابٍ زائدٍ للمستخدم في الواجهة.
 *
 * جاهزة للاستهلاك عبر zodResolver مباشرة (exports جاهزة لـ react-hook-form).
 */
import { z } from 'zod';

/** رسائل عربية حرفية من RegisterRequest::messages() — :max/:min مُعوَّضتان بـ255/8 */
const MESSAGES = {
  nameRequired: 'الاسم مطلوب.',
  nameMax: 'الاسم يجب ألا يتجاوز 255 حرفاً.',
  emailRequired: 'البريد الإلكتروني مطلوب.',
  emailInvalid: 'صيغة البريد الإلكتروني غير صحيحة.',
  emailMax: 'البريد الإلكتروني يجب ألا يتجاوز 255 حرفاً.',
  passwordRequired: 'كلمة المرور مطلوبة.',
  passwordMin: 'كلمة المرور يجب ألا تقل عن 8 أحرف.',
  passwordConfirmed: 'تأكيد كلمة المرور غير مطابق.',
} as const;

/**
 * مطابق لـ RegisterRequest::rules() حرفياً:
 *   name:     required | string | max:255
 *   email:    required | string | lowercase | email | max:255 | unique:users,email ← unique يتحقق منه الخادم فقط (422 مع fields.email)
 *   password: required | string | min:8 | confirmed
 *
 * ملاحظة "confirmed": Laravel يفشل عند غياب/اختلاف التأكيد برسالة واحدة
 * ('تأكيد كلمة المرور غير مطابق.') — لذا لا رسالة required منفصلة للتأكيد،
 * بل شرط تساوٍ واحد على المسار password_confirmation (مطابقة سلوكية حرفية).
 */
export const registerSchema = z
  .object({
    name: z.string().min(1, MESSAGES.nameRequired).max(255, MESSAGES.nameMax),
    email: z
      .string()
      .min(1, MESSAGES.emailRequired)
      .max(255, MESSAGES.emailMax)
      .email(MESSAGES.emailInvalid),
    password: z.string().min(1, MESSAGES.passwordRequired).min(8, MESSAGES.passwordMin),
    password_confirmation: z.string(),
  })
  .superRefine((data, ctx) => {
    // مكافئ قاعدة confirmed — الرسالة الحرفية من RegisterRequest::messages()
    if (data.password !== data.password_confirmation) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['password_confirmation'],
        message: MESSAGES.passwordConfirmed,
      });
    }
  });

/**
 * مطابق لـ LoginRequest::rules() حرفياً — انتبه للفروقات المقصودة عن Register:
 *   email:    required | string | lowercase | email   ← بلا max:255 (لم يشترطه LoginRequest)
 *   password: required | string                        ← بلا min:8 (التحقق الحقيقي ضد hash في الخادم)
 */
export const loginSchema = z.object({
  email: z.string().min(1, MESSAGES.emailRequired).email(MESSAGES.emailInvalid),
  password: z.string().min(1, MESSAGES.passwordRequired),
});

/** نوع مدخلات التسجيل — جاهز لـ useForm<RegisterInput> */
export type RegisterInput = z.infer<typeof registerSchema>;

/** نوع مدخلات الدخول — جاهز لـ useForm<LoginInput> */
export type LoginInput = z.infer<typeof loginSchema>;

/**
 * تطبيع البريد قبل الإرسال (trim + lowercase) — يجعل قاعدة lowercase الخلفية
 * مستوفاة تلقائياً فلا تصل رسالتها للمستخدم أصلاً (قرار موثّق أعلاه).
 */
export function normalizeEmail(email: string): string {
  return email.trim().toLowerCase();
}
