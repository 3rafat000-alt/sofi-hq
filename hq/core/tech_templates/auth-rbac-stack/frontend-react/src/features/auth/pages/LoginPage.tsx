/**
 * صفحة تسجيل الدخول — بطاقة وسط الشاشة، RTL عربي، dark-mode ready عبر tokens
 * الـCSS variables (--background/--card/--primary/...) المعرّفة في README.md.
 */
import { Link, useNavigate } from 'react-router-dom';
import { LoginForm } from '../components/LoginForm';

/** المسار بعد الدخول الناجح — عدّله لوجهة تطبيقك */
const AFTER_LOGIN_PATH = '/';

export default function LoginPage() {
  const navigate = useNavigate();

  return (
    <main dir="rtl" className="grid min-h-screen place-items-center bg-background px-4 py-10">
      <div className="w-full max-w-md space-y-6 rounded-xl border border-border bg-card p-8 text-card-foreground shadow-sm">
        <header className="space-y-1.5 text-center">
          <h1 className="text-2xl font-bold tracking-tight">تسجيل الدخول</h1>
          <p className="text-sm text-muted-foreground">
            أدخل بيانات حسابك للمتابعة إلى مساحتك.
          </p>
        </header>

        <LoginForm onSuccess={() => navigate(AFTER_LOGIN_PATH)} />

        <footer className="text-center text-sm text-muted-foreground">
          ليس لديك حساب؟{' '}
          <Link
            to="/register"
            className="font-medium text-primary underline-offset-4 hover:underline"
          >
            أنشئ حساباً جديداً
          </Link>
        </footer>
      </div>
    </main>
  );
}
