<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

/**
 * Registration rules per work order: strong email + min:8 confirmed password.
 * Bilingual messages: Arabic → error.fields of Envelope v1,
 * English counterparts kept beside them (messagesEn).
 */
class RegisterRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // public endpoint
    }

    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'string', 'lowercase', 'email', 'max:255', 'unique:users,email'],
            'password' => ['required', 'string', 'min:8', 'confirmed'],
        ];
    }

    public function messages(): array
    {
        return [
            'name.required' => 'الاسم مطلوب.',
            'name.string' => 'الاسم يجب أن يكون نصاً.',
            'name.max' => 'الاسم يجب ألا يتجاوز :max حرفاً.',
            'email.required' => 'البريد الإلكتروني مطلوب.',
            'email.lowercase' => 'يجب كتابة البريد الإلكتروني بأحرف صغيرة.',
            'email.email' => 'صيغة البريد الإلكتروني غير صحيحة.',
            'email.max' => 'البريد الإلكتروني يجب ألا يتجاوز :max حرفاً.',
            'email.unique' => 'هذا البريد الإلكتروني مسجل مسبقاً.',
            'password.required' => 'كلمة المرور مطلوبة.',
            'password.min' => 'كلمة المرور يجب ألا تقل عن :min أحرف.',
            'password.confirmed' => 'تأكيد كلمة المرور غير مطابق.',
        ];
    }

    public function messagesEn(): array
    {
        return [
            'name.required' => 'The name is required.',
            'name.string' => 'The name must be a string.',
            'name.max' => 'The name must not exceed :max characters.',
            'email.required' => 'The email address is required.',
            'email.lowercase' => 'The email must be written in lowercase letters.',
            'email.email' => 'Invalid email address format.',
            'email.max' => 'The email must not exceed :max characters.',
            'email.unique' => 'This email address is already registered.',
            'password.required' => 'The password is required.',
            'password.min' => 'The password must be at least :min characters.',
            'password.confirmed' => 'The password confirmation does not match.',
        ];
    }
}
