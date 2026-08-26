/// ════════════════════════════════════════════════════════════════════════
/// SOFI Auth Template — نقطة انطلاق طبقة المصادقة (المرحلة 3ب).
///
/// قرار إدارة الحالة: ChangeNotifier + provider — المبرر الكامل موثق
/// في رأس `features/auth/presentation/providers/auth_provider.dart`
/// (البساطة بلا codegen لقالب مرجعي).
///
/// الحزم الخارجية (ثلاث فقط، التفاصيل في PUBSPEC-SNIPPET.md):
///   http · provider · shared_preferences
///
/// التشغيل:
///   flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/v1
///   (معيار STACKS.md: baseUrl عبر --dart-define لا ملف .env)
/// ════════════════════════════════════════════════════════════════════════
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'core/storage/token_storage.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/data/repositories/auth_repository.dart';
import 'features/auth/presentation/providers/auth_provider.dart';
import 'features/auth/presentation/screens/login_screen.dart';
import 'features/auth/presentation/screens/register_screen.dart';

/// عنوان الخادم — يُمرَّر وقت البناء ويُستبدل بالافتراضي عند غيابه.
const String kApiBaseUrl = String.fromEnvironment(
  'API_BASE_URL',
  defaultValue: 'http://10.0.2.2:8000/api/v1',
);

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // تخزين التوكن: نسخة ذاكرة للقراءة المتزامنة + SharedPreferences للثبات.
  final prefs = await SharedPreferences.getInstance();
  final sessionStore = SessionStore(prefs);

  // التجميع اليدوي البسيط (بلا get_it عمداً): client ← repository ← provider.
  final apiClient = ApiClient(
    baseUrl: kApiBaseUrl,
    tokenProvider: sessionStore.cachedToken,
  );
  final authRepository = AuthRepository(apiClient);

  runApp(
    MultiProvider(
      providers: [
        Provider<TokenStorage>.value(value: sessionStore),
        ChangeNotifierProvider(
          create: (_) => AuthProvider(authRepository, sessionStore),
        ),
      ],
      child: const SofiAuthApp(),
    ),
  );
}

class SofiAuthApp extends StatelessWidget {
  const SofiAuthApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SOFI Auth',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light(), // مصدر الواجهة الوحيد.
      locale: const Locale('ar'),

      // RTL إجباري على كامل الشجرة (بلا flutter_localizations — خارج الحزم المسموحة).
      builder: (context, child) => Directionality(
        textDirection: TextDirection.rtl,
        child: child ?? const SizedBox.shrink(),
      ),

      initialRoute: '/',
      routes: {
        // بوابة الإقلاع: توكن محفوظ؟ → تحقق عبر /me → home : login.
        '/': (context) => const _BootGate(),
        '/login': (context) => const LoginScreen(),
        '/register': (context) => const RegisterScreen(),
        '/home': (context) => const _HomeScreen(),
      },
    );
  }
}

/// شاشة الإقلاع المؤقتة — حالة الاتصال ظاهرة (مؤشر تحميل) حتى ينتهي فحص الجلسة.
class _BootGate extends StatefulWidget {
  const _BootGate();

  @override
  State<_BootGate> createState() => _BootGateState();
}

class _BootGateState extends State<_BootGate> {
  @override
  void initState() {
    super.initState();
    // بعد أول إطار فقط — تغيير الـNavigator أثناء البناء ممنوع.
    WidgetsBinding.instance.addPostFrameCallback((_) => _restore());
  }

  Future<void> _restore() async {
    final authenticated = await context.read<AuthProvider>().restoreSession();
    if (!mounted) return;
    Navigator.of(context)
        .pushReplacementNamed(authenticated ? '/home' : '/login');
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('SOFI', style: textTheme.headlineMedium),
            const SizedBox(height: 24),
            CircularProgressIndicator(color: colorScheme.primary),
          ],
        ),
      ),
    );
  }
}

/// شاشة منزل مؤقتة لإتمام تدفق المصادقة — تُستبدل بشاشات الميزات القادمة.
/// تعرض ما يعيده العقد فعلياً: المستخدم + الدور + الصلاحيات المسطحة.
class _HomeScreen extends StatelessWidget {
  const _HomeScreen();

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    // درع حماية: لا يُرسم محتوى المنزل بلا مستخدم (مثلاً جلسة مُسحت أثناء العرض).
    final user = auth.user;
    if (user == null) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    final textTheme = Theme.of(context).textTheme;
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(title: const Text('الرئيسية')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(user.name, style: textTheme.titleLarge),
                  const SizedBox(height: 4),
                  Text(user.email, style: textTheme.bodyMedium),
                  if (user.role != null) ...[
                    const SizedBox(height: 12),
                    Chip(
                      label: Text(user.role!.displayName),
                      backgroundColor: colorScheme.primaryContainer,
                      labelStyle:
                          TextStyle(color: colorScheme.onPrimaryContainer),
                    ),
                  ],
                ],
              ),
            ),
          ),
          const SizedBox(height: 8),
          if (user.permissions.isNotEmpty)
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final permission in user.permissions)
                  Chip(label: Text(permission)),
              ],
            )
          else
            Text(
              'لا صلاحيات إضافية',
              style: textTheme.bodyMedium
                  ?.copyWith(color: colorScheme.onSurfaceVariant),
            ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: () async {
              await context.read<AuthProvider>().logout();
              if (context.mounted) {
                Navigator.of(context)
                    .pushNamedAndRemoveUntil('/login', (_) => false);
              }
            },
            icon: Icon(Icons.logout, color: colorScheme.onPrimary),
            label: const Text('تسجيل الخروج'),
          ),
        ],
      ),
    );
  }
}
