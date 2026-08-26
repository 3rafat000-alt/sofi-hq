/**
 * صفحة إنشاء الحساب — بطاقة وسط الشاشة، RTL عربي، dark-mode ready عبر tokens
 * الـCSS variables (--background/--card/--primary/...) المعرّفة في README.md.
 */
import { Link, useNavigate } from 'react-router-dom';
import { RegisterForm } from '../components/RegisterForm';

/** المسار بعد نجاح التسجيل — العقد يعيد جلسة كاملة فنوجّه مباشرة */
const AFTER_REGISTER_PATH = '/';

export default function RegisterPage() {
  const navigate = useNavigate();

  return (
    <main dir="rtl" className="grid min-h-screen place-items-center bg-background px-4 py-10">
      <div className="w-full max-w-md space-y-6 rounded-xl border border-border bg-card p-8 text-card-foreground shadow-sm">
        <header className="space-y-1.5 text-center">
          <h1 className="text-2xl font-bold tracking-tight">إنشاء حساب جديد</h1>
          <p className="text-sm text-muted-foreground">
            املأ البيانات التالية وستدخل إلى حسابك مباشرة بعد الإنشاء.
          </p>
        </header>

        <RegisterForm onSuccess={() => navigate(AFTER_REGISTER_PATH)} />

        <footer className="text-center text-sm text-muted-foreground">
          لديك حساب بالفعل؟{' '}
          <Link
            to="/login"
            className="font-medium text-primary underline-offset-4 hover:underline"
          >
            سجّل الدخول
          </Link>
        </footer>
      </div>
    </main>
  );
}
