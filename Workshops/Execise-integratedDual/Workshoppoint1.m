% =========================================================================
% CÁLCULO DEL POTENCIAL VECTORIAL MAGNÉTICO
% Conductor recto finito con corriente constante
% Autor: Cálculo analítico y numérico (Riemann N=10)
% =========================================================================

clear; clc; close all;

% =========================================================================
% DATOS DEL PROBLEMA
% =========================================================================
I = 3.0;      % Corriente en Amperes
x = 0.05;     % Coordenada x en metros
y = 0.03;     % Coordenada y en metros
z = 0.1;      % Coordenada z en metros
L1 = 0.5;     % Límite inferior del conductor en metros
L2 = 0.5;     % Límite superior del conductor en metros
mu0 = 4*pi*1e-7;  % Permeabilidad magnética del vacío (H/m)

% Cálculo de R
R_squared = x^2 + y^2;
R = sqrt(R_squared);

fprintf('============================================================\n');
fprintf('     POTENCIAL VECTORIAL MAGNÉTICO - CONDUCTOR FINITO\n');
fprintf('============================================================\n\n');
fprintf('DATOS DEL PROBLEMA:\n');
fprintf('  Corriente I = %.1f A\n', I);
fprintf('  Punto de observación: (%.2f, %.2f, %.2f) m\n', x, y, z);
fprintf('  Conductor: z'' ∈ [%.1f, %.1f] m\n', -L1, L2);
fprintf('  R = √(x² + y²) = %.8f m\n', R);
fprintf('  μ₀ = %.6e H/m\n', mu0);

% =========================================================================
% SOLUCIÓN ANALÍTICA
% =========================================================================
fprintf('\n============================================================\n');
fprintf('               SOLUCIÓN ANALÍTICA\n');
fprintf('============================================================\n');

% Términos dentro de los logaritmos
term1_arg = L2 - z;
term1_sqrt = sqrt(R_squared + (L2 - z)^2);
term1_log_arg = term1_arg + term1_sqrt;

term2_arg = -L1 - z;
term2_sqrt = sqrt(R_squared + (-L1 - z)^2);
term2_log_arg = term2_arg + term2_sqrt;

% Logaritmos
ln1 = log(term1_log_arg);
ln2 = log(term2_log_arg);

% Integral
integral_analitica = ln1 - ln2;

% Factor prefactor
prefactor = (mu0 * I) / (4 * pi);

% Potencial vectorial Az
Az_analitico = prefactor * integral_analitica;

fprintf('\nCálculos intermedios:\n');
fprintf('  L₂ - z = %.1f\n', term1_arg);
fprintf('  √(R² + (L₂-z)²) = %.6f\n', term1_sqrt);
fprintf('  ln(%.6f) = %.10f\n\n', term1_log_arg, ln1);
fprintf('  -L₁ - z = %.1f\n', term2_arg);
fprintf('  √(R² + (-L₁-z)²) = %.6f\n', term2_sqrt);
fprintf('  ln(%.6f) = %.10f\n', term2_log_arg, ln2);
fprintf('\n  Integral = %.10f\n', integral_analitica);
fprintf('  Prefactor μ₀I/(4π) = %.10e\n', prefactor);
fprintf('\n************************************************************\n');
fprintf('              RESULTADO ANALÍTICO\n');
fprintf('************************************************************\n');
fprintf('  Az = %.10e Wb/m\n', Az_analitico);
fprintf('  A⃗  = %.6e â_z Wb/m\n', Az_analitico);
fprintf('************************************************************\n');

% =========================================================================
% SOLUCIÓN NUMÉRICA (RIEMANN N=10)
% =========================================================================
fprintf('\n============================================================\n');
fprintf('         SOLUCIÓN NUMÉRICA - RIEMANN (N=10)\n');
fprintf('============================================================\n');

N = 10;  % Número de subintervalos
z_inf = -L1;
z_sup = L2;
delta_z = (z_sup - z_inf) / N;

% Puntos medios de cada subintervalo
z_primas = linspace(z_inf + delta_z/2, z_sup - delta_z/2, N);

% Suma de Riemann
suma_riemann = 0;
contribuciones = zeros(1, N);

fprintf('\nΔz'' = %.2f m\n', delta_z);
fprintf('\nContribuciones por subintervalo:\n');
fprintf('  i    z''_i (m)   distancia (m)     término\n');
fprintf('-----------------------------------------------------\n');

for i = 1:N
    zp = z_primas(i);
    distancia = sqrt(R_squared + (z - zp)^2);
    termino = delta_z / distancia;
    suma_riemann = suma_riemann + termino;
    contribuciones(i) = termino;
    fprintf('%3d   %8.3f     %12.8f   %15.10f\n', i, zp, distancia, termino);
end

Az_numerico = prefactor * suma_riemann;

fprintf('\n  Suma de Riemann = %.10f\n', suma_riemann);
fprintf('\n************************************************************\n');
fprintf('            RESULTADO NUMÉRICO (N=10)\n');
fprintf('************************************************************\n');
fprintf('  Az = %.10e Wb/m\n', Az_numerico);
fprintf('  A⃗  = %.6e â_z Wb/m\n', Az_numerico);
fprintf('************************************************************\n');

% =========================================================================
% COMPARACIÓN DE RESULTADOS
% =========================================================================
fprintf('\n============================================================\n');
fprintf('            COMPARACIÓN DE RESULTADOS\n');
fprintf('============================================================\n\n');

error_absoluto = abs(Az_analitico - Az_numerico);
error_relativo = (error_absoluto / abs(Az_analitico)) * 100;

fprintf('  Solución Analítica:  %.10e Wb/m\n', Az_analitico);
fprintf('  Solución Numérica:   %.10e Wb/m\n', Az_numerico);
fprintf('\n  Error absoluto:      %.10e Wb/m\n', error_absoluto);
fprintf('  Error relativo:      %.4f %%\n', error_relativo);
fprintf('\n============================================================\n');

% =========================================================================
% ANÁLISIS DE CONVERGENCIA
% =========================================================================
fprintf('\n============================================================\n');
fprintf('            ANÁLISIS DE CONVERGENCIA\n');
fprintf('============================================================\n\n');

N_valores = [5, 10, 20, 50, 100, 200, 500];
Az_numericos = zeros(size(N_valores));
errores_relativos = zeros(size(N_valores));

fprintf('   N    Az numérico (Wb/m)    Error relativo (%%)\n');
fprintf('-----------------------------------------------------\n');

for idx = 1:length(N_valores)
    n = N_valores(idx);
    dz = (z_sup - z_inf) / n;
    zps = linspace(z_inf + dz/2, z_sup - dz/2, n);
    suma = 0;
    for k = 1:n
        suma = suma + dz / sqrt(R_squared + (z - zps(k))^2);
    end
    Az_numericos(idx) = prefactor * suma;
    errores_relativos(idx) = abs(Az_analitico - Az_numericos(idx)) / abs(Az_analitico) * 100;
    fprintf('%4d   %.10e      %.6f\n', n, Az_numericos(idx), errores_relativos(idx));
end

% =========================================================================
% VISUALIZACIONES
% =========================================================================
fprintf('\n============================================================\n');
fprintf('              GENERANDO GRÁFICAS...\n');
fprintf('============================================================\n\n');

figure('Position', [100, 100, 1200, 900]);

% Gráfica 1: Contribuciones por subintervalo
subplot(2, 2, 1);
bar(1:N, contribuciones, 'FaceColor', [0.2, 0.4, 0.6], 'EdgeColor', 'k');
xlabel('Subintervalo i', 'FontSize', 11);
ylabel('Contribución', 'FontSize', 11);
title('Contribuciones de cada subintervalo (N=10)', 'FontSize', 12, 'FontWeight', 'bold');
grid on;
set(gca, 'FontSize', 10);

% Gráfica 2: Distribución de puntos de integración
subplot(2, 2, 2);
hold on;
plot([-L1, L2], [0, 0], 'k-', 'LineWidth', 3, 'DisplayName', 'Conductor');
plot([-L1, -L1], [-0.01, 0.01], 'g--', 'LineWidth', 2, 'DisplayName', 'Límites conductor');
plot([L2, L2], [-0.01, 0.01], 'g--', 'LineWidth', 2, 'HandleVisibility', 'off');
scatter(z_primas, zeros(1, N), 100, 'r', 'filled', 'DisplayName', 'Puntos medios');
scatter(z, 0, 150, 'b', 'p', 'filled', 'DisplayName', sprintf('Proyección (%g,%g,%g)', x, y, z));
xlabel('z'' (m)', 'FontSize', 11);
title('Distribución de puntos de integración', 'FontSize', 12, 'FontWeight', 'bold');
legend('Location', 'best', 'FontSize', 9);
grid on;
ylim([-0.02, 0.02]);
set(gca, 'FontSize', 10);
hold off;

% Gráfica 3: Convergencia con diferentes N
subplot(2, 2, 3);
semilogx(N_valores, errores_relativos, 'o-', 'Color', [0.8, 0.1, 0.2], 'LineWidth', 2, 'MarkerSize', 8, 'MarkerFaceColor', [0.8, 0.1, 0.2]);
hold on;
yline(error_relativo, 'b--', 'LineWidth', 1.5, 'Label', sprintf('N=10: %.4f%%', error_relativo));
xlabel('Número de subintervalos (N)', 'FontSize', 11);
ylabel('Error Relativo (%)', 'FontSize', 11);
title('Convergencia del método de Riemann', 'FontSize', 12, 'FontWeight', 'bold');
grid on;
set(gca, 'FontSize', 10);
hold off;

% Gráfica 4: Función integranda
subplot(2, 2, 4);
z_continuo = linspace(-L1, L2, 500);
integranda = 1 ./ sqrt(R_squared + (z - z_continuo).^2);
integranda_puntos = 1 ./ sqrt(R_squared + (z - z_primas).^2);

hold on;
plot(z_continuo, integranda, 'b-', 'LineWidth', 2, 'DisplayName', 'Función integranda');
scatter(z_primas, integranda_puntos, 80, 'r', 'filled', 'DisplayName', 'Puntos evaluados (N=10)');
xlabel('z'' (m)', 'FontSize', 11);
ylabel('1/√(R² + (z-z'')²)', 'FontSize', 11);
title('Función integranda y puntos de evaluación', 'FontSize', 12, 'FontWeight', 'bold');
legend('Location', 'best', 'FontSize', 9);
grid on;
set(gca, 'FontSize', 10);
hold off;

% Ajustar espaciado
sgtitle('Análisis del Potencial Vectorial Magnético', 'FontSize', 14, 'FontWeight', 'bold');

% =========================================================================
% RESUMEN FINAL
% =========================================================================
fprintf('\n============================================================\n');
fprintf('                  RESUMEN FINAL\n');
fprintf('============================================================\n\n');
fprintf('El potencial vectorial magnético en el punto (%.2f, %.2f, %.2f) m\n', x, y, z);
fprintf('debido a un conductor recto finito de longitud %.1f m\n', L1 + L2);
fprintf('con corriente %.1f A es:\n\n', I);
fprintf('  A⃗ = %.6e â_z Wb/m\n\n', Az_analitico);
fprintf('✓ El método numérico con N=10 aproxima con error: %.4f%%\n', error_relativo);
fprintf('✓ La componente es puramente axial (dirección ẑ)\n');
fprintf('✓ La convergencia mejora al aumentar N\n');
fprintf('\n============================================================\n');
fprintf('              CÁLCULO COMPLETADO ✓\n');
fprintf('============================================================\n');