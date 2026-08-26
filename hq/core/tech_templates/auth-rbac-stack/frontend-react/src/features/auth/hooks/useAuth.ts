/**
 * Server State للمصادقة عبر TanStack Query حصراً (قاعدة الغرفة):
 *   - القراءة:  useMe عبر useQuery — الهوية تُجلَب من الخادم ولا تُنسَخ إلى مخزن عميل.
 *   - الكتابة:  useLogin / useRegister / useLogout / useAssignRole عبر useMutation.
 *
 * التوكن credential وليس Server State — يُدار في authApi (localStorage) وهو من
 * يبني ترويسة Authorization؛ هنا فقط نضبطه/نمسحه في لحظات دوران الجلسة الصحيحة.
 *
 * مفاتيح الاستعلام موحّدة في authKeys — نقطة تسمية واحدة لكل ذاكرة المصادقة.
 */
import {
  useMutation,
  useQuery,
  useQueryClient,
  type QueryClient,
} from '@tanstack/react-query';
import * as authApi from '../api/authApi';
import type { AuthData, LoginPayload, RegisterPayload, RoleName } from '../types';

/** مفاتيح استعلام المصادقة الموحّدة */
export const authKeys = {
  all: ['auth'] as const,
  me: ['auth', 'me'] as const,
} as const;

// أدوات التوكن تعيش في authApi (مالك ترويسة Authorization) — يُعاد تصديرها لنقطة استهلاك واحدة
export {
  AuthApiError,
  TOKEN_STORAGE_KEY,
  clearToken,
  getToken,
  setToken,
} from '../api/authApi';

/**
 * الهوية الحالية — تعمل فقط عند وجود توكن.
 * retry:false لأن UNAUTHENTICATED لا يُعاد محاولته أبداً (المغلف نظّف التوكن أصلاً
 * داخل unwrapEnvelope) — الاستهلاك يتوجّه لتسجيل الدخول عند error + غياب data.
 */
export function useMe(options: { enabled?: boolean } = {}) {
  return useQuery({
    queryKey: authKeys.me,
    queryFn: ({ signal }) => authApi.me({ signal }),
    enabled: authApi.getToken() !== null && (options.enabled ?? true),
    retry: false,
    staleTime: 5 * 60 * 1000,
  });
}

/** تبنّي الجلسة بعد نجاح الدخول/التسجيل: حفظ التوكن + تحديث ذاكرة الهوية من استجابة الـmutation مباشرة */
function adoptSession(queryClient: QueryClient, data: AuthData): void {
  authApi.setToken(data.token);
  queryClient.setQueryData(authKeys.me, data.user);
}

/** POST /login — يخزّن التوكن ويملأ هوية المستخدم فوراً من نفس الاستجابة */
export function useLogin() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: LoginPayload) => authApi.login(payload),
    onSuccess: (data) => adoptSession(queryClient, data),
  });
}

/** POST /register — سلوك مطابق للدخول (العقد يعيد token + user أيضاً) */
export function useRegister() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: RegisterPayload) => authApi.register(payload),
    onSuccess: (data) => adoptSession(queryClient, data),
  });
}

/**
 * POST /logout — التنظيف المحلي في onSettled حتى لو فشل نداء revoke:
 * أشهر سبب لفشله توكن ميت أصلاً، وتنظيفه محلياً صحيح في الحالتين
 * (مطابق لملاحظة العقد الملزمة 4).
 */
export function useLogout() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => authApi.logout(),
    onSettled: () => {
      authApi.clearToken();
      queryClient.removeQueries({ queryKey: authKeys.all });
    },
  });
}

/**
 * PUT /users/{user}/role — تغيير دور مستخدم آخر (super-admin | manager فقط،
 * والبوابة الخلفية تفرضها). دور المستخدم الآخر لا يمس هويتنا، وذاكرة قوائم
 * المستخدمين ستملكها ميزة users لاحقاً — لذا لا نلمس ذاكرة المصادقة هنا.
 */
export function useAssignRole() {
  return useMutation({
    mutationFn: ({ userId, role }: { userId: number; role: RoleName }) =>
      authApi.assignRole(userId, { role }),
  });
}
