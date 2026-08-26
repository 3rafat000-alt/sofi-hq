<?php

use App\Http\Controllers\Api\AuthController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API routes — base /api/v1 (matches meta.api_version = "v1")
|--------------------------------------------------------------------------|
*/

Route::prefix('v1')->group(function () {
    /* Public — first-party clients (SPA/mobile) obtain tokens here.
       Throttled to blunt credential-stuffing on both endpoints. */
    Route::post('/register', [AuthController::class, 'register'])->middleware('throttle:10,1');
    Route::post('/login', [AuthController::class, 'login'])->middleware('throttle:10,1');

    /* Authenticated token holders only. */
    Route::middleware('auth:sanctum')->group(function () {
        Route::post('/logout', [AuthController::class, 'logout']);
        Route::get('/me', [AuthController::class, 'me']);

        /* Managers only — super-admin | manager (alias registered in bootstrap/app.php). */
        Route::put('/users/{user}/role', [AuthController::class, 'assignRole'])
            ->middleware('role:super-admin,manager');
    });
});
