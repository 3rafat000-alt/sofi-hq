/// شاشة إنشاء حساب — POST /register وفق العقد.
///
/// قواعد الغرفة المنفذة هنا:
/// - صفر قيم صلبة: كل الأنماط من `Theme.of(context)` حصراً.
/// - حالات الاتصال ظاهرة: مؤشر تحميل داخل الزر أثناء النداء وتعطيله.
/// - الأخطاء من العقد: messageAr للعرض، وerror.fields تُلحق بالرسالة.
/// - التسجيل الناجح يعيد توكن فورياً (AuthData) ⇒ دخول تلقائي إلى /home.
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/auth_provider.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmationController = TextEditingController();

  /// مطابق لقاعدة email في العقد (format: email).
  static final RegExp _emailRegExp = RegExp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$');

  // رسائل التحقق العربية — مطابقة حرفياً لرسائل RegisterRequest في الخادم
  // وقيم error.fields في أمثلة العقد (min:8، تأكيد كلمة المرور).
  static const String _nameRequired = 'الاسم مطلوب.';
  static const String _nameTooLong = 'الاسم يجب ألا يتجاوز 255 حرفاً.';
  static const String _emailRequired = 'البريد الإلكتروني مطلوب.';
  static const String _emailInvalid = 'صيغة البريد الإلكتروني غير صحيحة.';
  static const String _passwordRequired = 'كلمة المرور مطلوبة.';
  static const String _passwordTooShort = 'كلمة المرور يجب ألا تقل عن 8 أحرف.';
  static const String _confirmationMismatch = 'تأكيد كلمة المرور غير مطابق.';

  @override
  void dispose() {
    _nameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmationController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    FocusManager.instance.primaryFocus?.unfocus();
    if (!_formKey.currentState!.validate()) return;

    final auth = context.read<AuthProvider>();
    final ok = await auth.register(
      name: _nameController.text.trim(),
      email: _emailController.text.trim(),
      password: _passwordController.text,
      passwordConfirmation: _confirmationController.text,
    );
    if (!mounted) return;

    if (ok) {
      // العقد يعيد توكن فورياً عند 201 — لا شاشة وسيطة، دخول مباشر.
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

  String? _validateName(String? value) {
    final name = value?.trim() ?? '';
    if (name.isEmpty) return _nameRequired;
    if (name.length > 255) return _nameTooLong; // max:255 في العقد.
    return null;
  }

  String? _validateEmail(String? value) {
    final email = value?.trim() ?? '';
    if (email.isEmpty) return _emailRequired;
    if (!_emailRegExp.hasMatch(email)) return _emailInvalid;
    return null;
  }

  String? _validatePassword(String? value) {
    if (value == null || value.isEmpty) return _passwordRequired;
    if (value.length < 8) return _passwordTooShort; // min:8 في العقد.
    return null;
  }

  String? _validateConfirmation(String? value) {
    // رسالة واحدة كما يرسلها الخادم لقاعدة confirmed.
    if (value == null ||
        value.isEmpty ||
        value != _passwordController.text) {
      return _confirmationMismatch;
    }
    return null;
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
                    'إنشاء حساب',
                    style: textTheme.headlineMedium,
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'خطوات قليلة وتصبح جزءاً منا',
                    style: textTheme.bodyMedium
                        ?.copyWith(color: colorScheme.onSurfaceVariant),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),
                  TextFormField(
                    controller: _nameController,
                    keyboardType: TextInputType.name,
                    textInputAction: TextInputAction.next,
                    autofillHints: const [AutofillHints.name],
                    decoration: const InputDecoration(labelText: 'الاسم'),
                    validator: _validateName,
                  ),
                  const SizedBox(height: 16),
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
                    textInputAction: TextInputAction.next,
                    autofillHints: const [AutofillHints.newPassword],
                    decoration: const InputDecoration(
                      labelText: 'كلمة المرور',
                    ),
                    validator: _validatePassword,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _confirmationController,
                    obscureText: true,
                    textInputAction: TextInputAction.done,
                    autofillHints: const [AutofillHints.newPassword],
                    onFieldSubmitted: (_) {
                      if (!auth.isLoading) _submit();
                    },
                    decoration: const InputDecoration(
                      labelText: 'تأكيد كلمة المرور',
                    ),
                    validator: _validateConfirmation,
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
                        : const Text('إنشاء الحساب'),
                  ),
                  const SizedBox(height: 16),
                  TextButton(
                    onPressed: auth.isLoading
                        ? null
                        : () =>
                            Navigator.of(context).pushReplacementNamed('/login'),
                    child: const Text('لديك حساب؟ سجّل دخولك'),
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
