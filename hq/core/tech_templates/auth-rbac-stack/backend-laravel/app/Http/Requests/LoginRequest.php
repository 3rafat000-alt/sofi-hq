<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

/**
 * Login rules: credentials are verified against the stored hash via Hash::check()
 * in the controller — input stays plain (unhashed), no min/confirmed here.
 * Bilingual messages: Arabic → error.fields, English counterparts beside them.
 */
class LoginRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // public endpoint
    }

    public function rules(): array
    {
        return [
            'email' => ['required', 'string', 'lowercase', 'email'],
            // Plain input only — never re-hashed before comparison.
            'password' => ['required', 'string'],
        ];
    }

    public function messages(): array
    {
        return [
            'email.required' => 'البريد الإلكتروني مطلوب.',
            'email.lowercase' => 'يجب كتابة البريد الإلكتروني بأحرف صغيرة.',
            'email.email' => 'صيغة البريد الإلكتروني غير صحيحة.',
            'password.required' => 'كلمة المرور مطلوبة.',
        ];
    }

    public function messagesEn(): array
    {
        return [
            'email.required' => 'The email address is required.',
            'email.lowercase' => 'The email must be written in lowercase letters.',
            'email.email' => 'Invalid email address format.',
            'password.required' => 'The password is required.',
        ];
    }
}
