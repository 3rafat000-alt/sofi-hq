# PUBSPEC-SNIPPET.md — mobile-flutter dependencies

The scope of phase 3B is the `lib/` sources exclusively; this is the official snippet for the
`pubspec.yaml` created on the first `flutter create .` inside this folder
(stack standard per stacks-tech.md: framework tooling fills in its own standard files).

## environment + dependencies (copy as-is)

```yaml
environment:
  sdk: ^3.5.0

dependencies:
  flutter:
    sdk: flutter

  # Networking — the backbone api_client.dart column (POST/GET on top of the v1 envelope).
  http: ^1.2.2

  # State management — ChangeNotifier Provider (decision documented atop auth_provider.dart).
  provider: ^6.1.2

  # Token storage across runs — behind the SessionStore abstraction in core/storage/.
  shared_preferences: ^2.3.2
```

## dev_dependencies (optional — for static analysis)

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0
```

## Strict rule

**Exactly three external packages**: `http` · `provider` · `shared_preferences`.
No dio, no get_it, no bloc, no google_fonts, no codegen — an RCCF decision
for a simple reference template that can be upgraded later without touching the contract layers.

## Running

```bash
flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000/api/v1
```

- `10.0.2.2` = the host's localhost from an Android emulator (Laravel: `php artisan serve`).
- iOS Simulator uses `http://127.0.0.1:8000/api/v1`.
