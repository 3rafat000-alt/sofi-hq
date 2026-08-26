/// شاشة تسجيل الدخول — POST /login وفق العقد.
///
/// قواعد الغرفة المنفذة هنا:
/// - صفر قيم صلبة: كل الأنماط من `Theme.of(context)` حصراً.
/// - حالات الاتصال ظاهرة: مؤشر تحميل داخل الزر أثناء النداء وتعطيله.
/// - الأخطاء من العقد: messageAr للعرض، وerror.fields تُلحق بالرسالة.
/// - RTL مفعّل على مستوى MaterialApp.builder في main.dart.
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/auth_provider.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  /// مطابق لقاعدة email في العقد (format: email).
  static final RegExp _emailRegExp = RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$');

  // رسائل التحقق العربية — مطابقة حرفياً لرسائل LoginRequest في الخادم
  // حتى يتطابق ما يراه المستخدم محلياً مع ما قد يعود من error.fields.
  static const String _emailRequired = 'البريد الإلكتروني مطلوب.';
  static const String _emailInvalid = 'صيغة البريد الإلكتروني غير صحيحة.';
  static const String _passwordRequired = 'كلمة المرور مطلوبة.';

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    FocusManager.instance.primaryFocus?.unfocus();
    if (!_formKey.currentState!.validate()) return;

    final auth = context.read<AuthProvider>();
    final ok = await auth.login(
      email: _emailController.text.trim(),
      password: _passwordController.text,
    );
    if (!mounted) return;

    if (ok) {
      Navigator.of(context).pushReplacementNamed('/home');
    } else {
      _showErrorSnackBar(auth);
    }
  }

  /// عرض خطأ الفشل من العقد: messageAr + أسطر error.fields إن وجدت.
  void _showErrorSnackBar(AuthProvider auth) {
    final colorScheme = Theme.of(context).colorScheme;
    final buffer = StringBuffer(auth.errorAr ?? 'حدث خطأ غير متوقع.');
    final fields = auth.fieldErrors;
    if (fields != null) {
      for (final messages in fields.values) {
        for (final message in messages) {
          buffer.write('\n• $message');
        }
      }
    }
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          content: Text(
            buffer.toString(),
            style: TextStyle(color: colorScheme.onError),
          ),
          backgroundColor: colorScheme.error,
        ),
      );
  }

  String? _validateEmail(String? value) {
    final email = value?.trim() ?? '';
    if (email.isEmpty) return _emailRequired;
    if (!_emailRegExp.hasMatch(email)) return _emailInvalid;
    return null;
  }

  String? _validatePassword(String? value) {
    if (value == null || value.isEmpty) return _passwordRequired;
    return null; // كلمة المرور بلا min محلياً — التحقق الفعلي لدى الخادم.
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthProvider>();
    final textTheme = Theme.of(context).textTheme;
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
            child: Form(
              key: _formKey,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'تسجيل الدخول',
                    style: textTheme.headlineMedium,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'أدخل بياناتك للمتابعة إلى حسابك',
                    style: textTheme.bodyMedium
                        ?.copyWith(color: colorScheme.onSurfaceVariant),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),
                  TextFormField(
                    controller: _emailController,
                    keyboardType: TextInputType.emailAddress,
                    textInputAction: TextInputAction.next,
                    autofillHints: const [AutofillHints.email],
                    decoration: const InputDecoration(
                      labelText: 'البريد الإلكتروني',
                    ),
                    validator: _validateEmail,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _passwordController,
                    obscureText: true,
                    textInputAction: TextInputAction.done,
                    autofillHints: const [AutofillHints.password],
                    onFieldSubmitted: (_) {
                      if (!auth.isLoading) _submit();
                    },
                    decoration: const InputDecoration(
                      labelText: 'كلمة المرور',
                    ),
                    validator: _validatePassword,
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton(
                    onPressed: auth.isLoading ? null : _submit,
                    child: auth.isLoading
                        ? SizedBox(
                            width: 22,
                            height: 22,
                            child: CircularProgressIndicator(
                              strokeWidth: 2.5,
                              color: colorScheme.onPrimary,
                            ),
                          )
                        : const Text('دخول'),
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: auth.isLoading
                        ? null
                        : () =>
                            Navigator.of(context).pushReplacementNamed('/register'),
                    child: const Text('ليس لديك حساب؟ أنشئ حساباً جديداً'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
