<?php

use App\Http\Middleware\EnsureUserHasRole;
use App\Http\Responses\ApiResponse;
use Illuminate\Auth\AuthenticationException;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;
use Illuminate\Http\Request;
use Illuminate\Http\Exceptions\ThrottleRequestsException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Symfony\Component\HttpKernel\Exception\AccessDeniedHttpException;
use Illuminate\Validation\ValidationException;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        api: __DIR__.'/../routes/api.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        // RBAC gate — usage: ->middleware('role:super-admin,manager')
        $middleware->alias([
            'role' => EnsureUserHasRole::class,
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions) {
        // Envelope v1: exceptions never leak raw to consumers (API-ENVELOPE.md).
        $exceptions->render(function (ValidationException $e, Request $request) {
            return ApiResponse::validationFailed($e->errors());
        });
        $exceptions->render(function (AuthenticationException $e, Request $request) {
            return ApiResponse::unauthenticated();
        });
        $exceptions->render(function (AuthorizationException|AccessDeniedHttpException $e, Request $request) {
            return ApiResponse::forbidden();
        });
        $exceptions->render(function (ModelNotFoundException|NotFoundHttpException $e, Request $request) {
            return ApiResponse::notFound();
        });
        $exceptions->render(function (ThrottleRequestsException $e, Request $request) {
            return ApiResponse::rateLimited();
        });
    })->create();
