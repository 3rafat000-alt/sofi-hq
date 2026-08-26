/**
 * نموذج إنشاء الحساب — react-hook-form + zodResolver(registerSchema).
 *
 * التدفق:
 *   1. تحقق Zod عميل مطابق حرفياً لـ RegisterRequest
 *      (name max:255 · email · password min:8 + confirmed).
 *   2. normalizeEmail قبل الإرسال (قرار schemas.ts الموثّق حول قاعدة lowercase).
 *   3. أخطاء الحقول الخلفية العربية (error.fields — مثل "البريد مسجل مسبقاً")
 *      تُدمج داخل الفورم على حقولها.
 *   4. رسالة messageAr العامة في شريط أعلى الفورم.
 *   5. الزر disabled + spinner أثناء isPending.
 */
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { AuthApiError } from '../api/authApi';
import { normalizeEmail, registerSchema, type RegisterInput } from '../schemas';
import { useRegister } from '../hooks/useAuth';
import type { AuthData } from '../types';

interface RegisterFormProps {
  /** يُستدعى بعد نجاح التسجيل — العقد يعيد جلسة كاملة (token + user) */
  onSuccess?: (data: AuthData) => void;
}

/* أنماط shadcn/ui-style فوق tokens الـCSS variables — dark-mode ready بلا CSS مخصص */
const FIELD_CLASS = 'space-y-2';
const LABEL_CLASS = 'block text-sm font-medium leading-none text-foreground';
const INPUT_CLASS =
  'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ring-offset-background disabled:cursor-not-allowed disabled:opacity-50 aria-[invalid=true]:border-destructive aria-[invalid=true]:focus-visible:ring-destructive';
const ERROR_CLASS = 'text-sm text-destructive';
const BANNER_CLASS =
  'rounded-md border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive';
const BUTTON_CLASS =
  'inline-flex h-10 w-full items-center justify-center gap-2 rounded-md bg-primary px-4 text-sm font-semibold text-primary-foreground shadow-sm transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ring-offset-background disabled:pointer-events-none disabled:opacity-50';

/** حقول النموذج القابلة لدمج أخطاء الخادم فيها — أسماؤها تطابق error.fields في العقد */
const FORM_FIELDS = ['name', 'email', 'password', 'password_confirmation'] as const;

function Spinner() {
  return (
    <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
      />
    </svg>
  );
}

export function RegisterForm({ onSuccess }: RegisterFormProps) {
  const registerMutation = useRegister();
  const [bannerError, setBannerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<RegisterInput>({
    resolver: zodResolver(registerSchema),
    defaultValues: { name: '', email: '', password: '', password_confirmation: '' },
  });

  const onSubmit = handleSubmit(async (values) => {
    setBannerError(null);
    try {
      // تطبيع البريد قبل الإرسال — انظر قرار lowercase في schemas.ts
      const data = await registerMutation.mutateAsync({
        name: values.name.trim(),
        email: normalizeEmail(values.email),
        password: values.password,
        password_confirmation: values.password_confirmation,
      });
      onSuccess?.(data);
    } catch (error) {
      if (!(error instanceof AuthApiError)) {
        setBannerError('حدث خطأ غير متوقع. حاول مجدداً.');
        return;
      }
      let mergedFieldError = false;
      for (const [field, messages] of Object.entries(error.fields ?? {})) {
        if (!(FORM_FIELDS as readonly string[]).includes(field)) continue;
        setError(field as keyof RegisterInput, { message: messages[0] ?? error.messageAr });
        mergedFieldError = true;
      }
      if (!mergedFieldError) setBannerError(error.messageAr);
    }
  });

  return (
    <form noValidate onSubmit={onSubmit} className="space-y-5">
      {bannerError !== null && (
        <div role="alert" className={BANNER_CLASS}>
          {bannerError}
        </div>
      )}

      <div className={FIELD_CLASS}>
        <label htmlFor="register-name" className={LABEL_CLASS}>
          الاسم
        </label>
        <input
          id="register-name"
          type="text"
          autoComplete="name"
          placeholder="اسمك الكامل"
          aria-invalid={errors.name ? true : undefined}
          aria-describedby={errors.name ? 'register-name-error' : undefined}
          className={INPUT_CLASS}
          {...register('name')}
        />
        {errors.name !== undefined && (
          <p id="register-name-error" className={ERROR_CLASS}>
            {errors.name.message}
          </p>
        )}
      </div>

      <div className={FIELD_CLASS}>
        <label htmlFor="register-email" className={LABEL_CLASS}>
          البريد الإلكتروني
        </label>
        <input
          id="register-email"
          type="email"
          dir="ltr"
          autoComplete="email"
          placeholder="name@example.com"
          aria-invalid={errors.email ? true : undefined}
          aria-describedby={errors.email ? 'register-email-error' : undefined}
          className={INPUT_CLASS}
          {...register('email')}
        />
        {errors.email !== undefined && (
          <p id="register-email-error" className={ERROR_CLASS}>
            {errors.email.message}
          </p>
        )}
      </div>

      <div className={FIELD_CLASS}>
        <label htmlFor="register-password" className={LABEL_CLASS}>
          كلمة المرور
        </label>
        <input
          id="register-password"
          type="password"
          autoComplete="new-password"
          aria-invalid={errors.password ? true : undefined}
          aria-describedby={errors.password ? 'register-password-error' : undefined}
          className={INPUT_CLASS}
          {...register('password')}
        />
        {errors.password !== undefined && (
          <p id="register-password-error" className={ERROR_CLASS}>
            {errors.password.message}
          </p>
        )}
      </div>

      <div className={FIELD_CLASS}>
        <label htmlFor="register-password-confirmation" className={LABEL_CLASS}>
          تأكيد كلمة المرور
        </label>
        <input
          id="register-password-confirmation"
          type="password"
          autoComplete="new-password"
          aria-invalid={
            errors.password !== undefined || errors.password_confirmation !== undefined
              ? true
              : undefined
          }
          aria-describedby={
            errors.password_confirmation !== undefined
              ? 'register-password-confirmation-error'
              : undefined
          }
          className={INPUT_CLASS}
          {...register('password_confirmation')}
        />
        {errors.password_confirmation !== undefined && (
          <p id="register-password-confirmation-error" className={ERROR_CLASS}>
            {errors.password_confirmation.message}
          </p>
        )}
      </div>

      <button type="submit" disabled={isSubmitting} className={BUTTON_CLASS}>
        {isSubmitting ? (
          <>
            <Spinner />
            جارٍ إنشاء الحساب…
          </>
        ) : (
          'إنشاء حساب جديد'
        )}
      </button>
    </form>
  );
}
