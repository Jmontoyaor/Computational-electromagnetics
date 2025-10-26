% =========================================================================
% MÉTODO DE ELEMENTOS FINITOS (MEF) - EJEMPLO 6.1
% Ensamblaje de matriz global para segmento con 5 nodos
% =========================================================================

clear; clc; close all;

fprintf('============================================================\n');
fprintf('     MÉTODO DE ELEMENTOS FINITOS (MEF)\n');
fprintf('     Ejemplo 6.1: Ensamblaje de Matriz Global\n');
fprintf('============================================================\n\n');

% =========================================================================
% DEFINICIÓN DE MATRICES ELEMENTALES SIMBÓLICAS
% =========================================================================

fprintf('PASO 1: Definición de Matrices Elementales\n');
fprintf('------------------------------------------------------------\n\n');

fprintf('Cada elemento conecta dos nodos consecutivos:\n');
fprintf('  Ω₁: nodos 1-2\n');
fprintf('  Ω₂: nodos 2-3\n');
fprintf('  Ω₃: nodos 3-4\n');
fprintf('  Ω₄: nodos 4-5\n\n');

% =========================================================================
% PROCESO DE ENSAMBLAJE PASO A PASO
% =========================================================================

fprintf('============================================================\n');
fprintf('PASO 2: Proceso de Ensamblaje Paso a Paso\n');
fprintf('============================================================\n\n');

fprintf('📍 NODO 1 - Solo pertenece a Ω₁\n');
fprintf('   Contribución: a[1]\n\n');

fprintf('📍 NODO 2 - Pertenece a Ω₁ y Ω₂ (SUMA DE CONTRIBUCIONES)\n');
fprintf('   Contribución: a₁₁[1] + a₀₀[2]\n\n');

fprintf('📍 NODO 3 - Pertenece a Ω₂ y Ω₃ (SUMA DE CONTRIBUCIONES)\n');
fprintf('   Contribución: a₁₁[2] + a₀₀[3]\n\n');

fprintf('📍 NODO 4 - Pertenece a Ω₃ y Ω₄ (SUMA DE CONTRIBUCIONES)\n');
fprintf('   Contribución: a₁₁[3] + a₀₀[4]\n\n');

fprintf('📍 NODO 5 - Solo pertenece a Ω₄\n');
fprintf('   Contribución: a[4]\n\n');

fprintf('============================================================\n');
fprintf('MATRIZ GLOBAL FINAL (Estructura Simbólica)\n');
fprintf('============================================================\n\n');

fprintf('       [  a₀₀[1]        a₀₁[1]           0              0              0        ]\n');
fprintf('       [  a₁₀[1]   a₁₁[1]+a₀₀[2]     a₀₁[2]           0              0        ]\n');
fprintf('   A = [    0         a₁₀[2]      a₁₁[2]+a₀₀[3]     a₀₁[3]           0        ]\n');
fprintf('       [    0            0            a₁₀[3]      a₁₁[3]+a₀₀[4]    a₀₁[4]     ]\n');
fprintf('       [    0            0               0            a₁₀[4]        a₁₁[4]    ]\n\n');

fprintf('✅ OBSERVACIONES:\n');
fprintf('  • Matriz TRIDIAGONAL (valores solo en diagonal y adyacentes)\n');
fprintf('  • Nodos interiores: SUMA de contribuciones de elementos vecinos\n');
fprintf('  • Nodos extremos: una sola contribución\n');
fprintf('  • Estructura característica de problemas 1D en MEF\n\n');

% =========================================================================
% EJEMPLO NUMÉRICO
% =========================================================================

fprintf('============================================================\n');
fprintf('PASO 3: Ejemplo Numérico\n');
fprintf('============================================================\n\n');

% Parámetros del problema
L_total = 1.0;      % Longitud total (m)
n_elementos = 4;    % Número de elementos
n_nodos = 5;        % Número de nodos
L_elem = L_total / n_elementos;  % Longitud por elemento
sigma = 1.0;        % Conductividad

fprintf('Parámetros:\n');
fprintf('  Longitud total: %.1f m\n', L_total);
fprintf('  Número de elementos: %d\n', n_elementos);
fprintf('  Número de nodos: %d\n', n_nodos);
fprintf('  Longitud por elemento: %.2f m\n', L_elem);
fprintf('  Conductividad σ: %.1f\n\n', sigma);

% Matriz elemental típica para elemento lineal 1D
% A_elem = (σ/L) * [[1, -1], [-1, 1]]
A_elem = (sigma / L_elem) * [1, -1; -1, 1];

fprintf('Matriz elemental numérica (σ/L):\n');
disp(A_elem);

% Inicializar matriz global
A_global = zeros(n_nodos, n_nodos);

% Ensamblaje elemento por elemento
fprintf('\nProceso de ensamblaje:\n');
fprintf('------------------------------------------------------------\n');

% Elemento 1: nodos 1-2 (índices 1-2 en MATLAB)
fprintf('Elemento 1 (Ω₁): nodos 1-2\n');
A_global(1:2, 1:2) = A_global(1:2, 1:2) + A_elem;
fprintf('  Contribución agregada\n\n');

% Elemento 2: nodos 2-3
fprintf('Elemento 2 (Ω₂): nodos 2-3\n');
A_global(2:3, 2:3) = A_global(2:3, 2:3) + A_elem;
fprintf('  Contribución agregada (nodo 2 suma con anterior)\n\n');

% Elemento 3: nodos 3-4
fprintf('Elemento 3 (Ω₃): nodos 3-4\n');
A_global(3:4, 3:4) = A_global(3:4, 3:4) + A_elem;
fprintf('  Contribución agregada (nodo 3 suma con anterior)\n\n');

% Elemento 4: nodos 4-5
fprintf('Elemento 4 (Ω₄): nodos 4-5\n');
A_global(4:5, 4:5) = A_global(4:5, 4:5) + A_elem;
fprintf('  Contribución agregada (nodo 4 suma con anterior)\n\n');

fprintf('============================================================\n');
fprintf('MATRIZ GLOBAL NUMÉRICA ENSAMBLADA (5×5)\n');
fprintf('============================================================\n');
disp(A_global);

fprintf('Verificación de estructura tridiagonal:\n');
fprintf('  Diagonal principal: [%.1f, %.1f, %.1f, %.1f, %.1f]\n', diag(A_global));
fprintf('  Diagonal superior:  [%.1f, %.1f, %.1f, %.1f]\n', diag(A_global, 1));
fprintf('  Diagonal inferior:  [%.1f, %.1f, %.1f, %.1f]\n\n', diag(A_global, -1));

% =========================================================================
% VISUALIZACIONES
% =========================================================================

fprintf('============================================================\n');
fprintf('GENERANDO VISUALIZACIONES...\n');
fprintf('============================================================\n\n');

figure('Position', [100, 100, 1400, 1000]);

% ----------------------------------------------------------------------
% Gráfica 1: Dominio discretizado
% ----------------------------------------------------------------------
subplot(3, 2, 1);
node_positions = linspace(0, L_total, n_nodos);
hold on;

% Dibujar elementos (líneas)
for i = 1:n_elementos
    plot([node_positions(i), node_positions(i+1)], [0, 0], 'b-', 'LineWidth', 3);
    mid = (node_positions(i) + node_positions(i+1)) / 2;
    text(mid, -0.05, sprintf('\\Omega_%d', i), 'HorizontalAlignment', 'center', ...
         'FontSize', 9, 'BackgroundColor', [0.7, 0.9, 1], 'EdgeColor', 'k');
end

% Dibujar nodos
plot(node_positions, zeros(1, n_nodos), 'ro', 'MarkerSize', 12, 'MarkerFaceColor', 'r');
for i = 1:n_nodos
    text(node_positions(i), 0.05, sprintf('Nodo %d', i), ...
         'HorizontalAlignment', 'center', 'FontSize', 10, 'FontWeight', 'bold');
end

xlim([-0.1, 1.1]);
ylim([-0.15, 0.15]);
xlabel('Posición (m)', 'FontSize', 11);
title('Discretización del Dominio (5 nodos, 4 elementos)', ...
      'FontSize', 12, 'FontWeight', 'bold');
grid on;
set(gca, 'YTick', []);
hold off;

% ----------------------------------------------------------------------
% Gráfica 2: Patrón de sparsidad
% ----------------------------------------------------------------------
subplot(3, 2, 2);
spy(A_global);
set(gca, 'FontSize', 10);
xlabel('Nodo j', 'FontSize', 11);
ylabel('Nodo i', 'FontSize', 11);
title('Patrón de Sparsidad (Estructura Tridiagonal)', ...
      'FontSize', 12, 'FontWeight', 'bold');
grid on;

% ----------------------------------------------------------------------
% Gráfica 3: Matriz global numérica con valores
% ----------------------------------------------------------------------
subplot(3, 2, 3);
imagesc(A_global);
colormap(gca, 'jet');
colorbar;
axis equal tight;
set(gca, 'XTick', 1:n_nodos, 'YTick', 1:n_nodos);
xlabel('Nodo j', 'FontSize', 11);
ylabel('Nodo i', 'FontSize', 11);
title('Matriz Global Numérica (valores)', 'FontSize', 12, 'FontWeight', 'bold');

% Añadir valores de texto
for i = 1:n_nodos
    for j = 1:n_nodos
        if A_global(i,j) ~= 0
            text(j, i, sprintf('%.1f', A_global(i,j)), ...
                 'HorizontalAlignment', 'center', 'Color', 'white', ...
                 'FontSize', 9, 'FontWeight', 'bold');
        end
    end
end

% ----------------------------------------------------------------------
% Gráfica 4: Proceso de ensamblaje
% ----------------------------------------------------------------------
subplot(3, 2, 4);
steps = 0:5;
nnz_counts = [0, 4, 8, 11, 14, 16];
plot(steps, nnz_counts, 'o-', 'LineWidth', 2, 'MarkerSize', 10, ...
     'Color', [0.2, 0.4, 0.6], 'MarkerFaceColor', [1, 0.6, 0]);
xlabel('Paso (nodo)', 'FontSize', 11);
ylabel('Elementos no nulos', 'FontSize', 11);
title('Crecimiento de la Matriz durante Ensamblaje', ...
      'FontSize', 12, 'FontWeight', 'bold');
grid on;
set(gca, 'XTick', 0:5, 'XTickLabel', {'Inicio', 'N1', 'N2', 'N3', 'N4', 'N5'});

% Añadir etiquetas de valores
for i = 1:length(steps)
    text(steps(i), nnz_counts(i) + 0.5, sprintf('%d', nnz_counts(i)), ...
         'HorizontalAlignment', 'center', 'FontSize', 9, 'FontWeight', 'bold');
end

% ----------------------------------------------------------------------
% Gráfica 5: Contribuciones por nodo
% ----------------------------------------------------------------------
subplot(3, 2, 5);
nodes = 1:n_nodos;
contributions = [1, 2, 2, 2, 1];
colors = [1, 0.5, 0.5; 0.5, 1, 0.5; 0.5, 1, 0.5; 0.5, 1, 0.5; 1, 0.5, 0.5];

b = bar(nodes, contributions, 'FaceColor', 'flat');
b.CData = colors;
b.EdgeColor = 'k';
b.LineWidth = 1.5;

xlabel('Nodo', 'FontSize', 11);
ylabel('Número de elementos', 'FontSize', 11);
title('Contribuciones de Elementos a cada Nodo', ...
      'FontSize', 12, 'FontWeight', 'bold');
ylim([0, 3]);
grid on;
set(gca, 'XTick', 1:n_nodos);

% Añadir etiquetas sobre barras
for i = 1:n_nodos
    text(i, contributions(i) + 0.15, sprintf('%d', contributions(i)), ...
         'HorizontalAlignment', 'center', 'FontSize', 11, 'FontWeight', 'bold');
end

% ----------------------------------------------------------------------
% Gráfica 6: Información de DOF
% ----------------------------------------------------------------------
subplot(3, 2, 6);
axis off;

info_text = {
    '\bf\fontsize{13}Grados de Libertad (DOF)'
    ''
    '\rm\fontsize{10}• Cada nodo = 1 DOF (potencial eléctrico)'
    '• Total DOF = 5 (para 5 nodos)'
    ''
    '• Elemento 1D lineal: 2 DOF/elemento'
    '• Conectividad: nodos consecutivos'
    ''
    '• Matriz global: N×N (N = nodos)'
    '• Estructura: Tridiagonal (1D)'
    ''
    '• Nodos interiores: suma de contribuciones'
    '• Nodos extremos: una sola contribución'
    ''
    '\bf\fontsize{11}Ecuación del sistema:'
    '\rm\fontsize{10}A · V = F'
    ''
    'A: Matriz global (rigidez)'
    'V: Vector de incógnitas (potenciales)'
    'F: Vector de términos fuente'
};

text(0.1, 0.95, info_text, 'Units', 'normalized', ...
     'VerticalAlignment', 'top', 'FontName', 'FixedWidth', ...
     'BackgroundColor', [1, 1, 0.9], 'EdgeColor', 'k', ...
     'Margin', 10);

% Título general
sgtitle('Método de Elementos Finitos - Ensamblaje de Matriz Global', ...
        'FontSize', 15, 'FontWeight', 'bold');

% =========================================================================
% SOLUCIÓN DE UN PROBLEMA EJEMPLO
% =========================================================================

fprintf('============================================================\n');
fprintf('PASO 4: Solución de un Problema Ejemplo\n');
fprintf('============================================================\n\n');

fprintf('Problema: Cable conductor con potencial fijo en extremos\n');
fprintf('  Condiciones de frontera:\n');
fprintf('    V(nodo 1) = 0 V\n');
fprintf('    V(nodo 5) = 10 V\n');
fprintf('  Sin fuentes internas (F = 0)\n\n');

% Aplicar condiciones de frontera (método de eliminación)
% Sistema modificado después de aplicar BC
A_reduced = A_global(2:4, 2:4);  % Submatriz para nodos interiores
F_reduced = zeros(3, 1);

% Contribuciones de los nodos con BC conocidas
F_reduced(1) = -A_global(2, 1) * 0;     % Contribución nodo 1 (V=0)
F_reduced(3) = -A_global(4, 5) * 10;    % Contribución nodo 5 (V=10)

fprintf('Sistema reducido (nodos interiores 2, 3, 4):\n');
fprintf('A_reduced:\n');
disp(A_reduced);
fprintf('F_reduced:\n');
disp(F_reduced);

% Resolver sistema
V_interior = A_reduced \ F_reduced;

% Vector de solución completo
V_completo = [0; V_interior; 10];

fprintf('\nSolución de potenciales nodales:\n');
for i = 1:n_nodos
    fprintf('  V(nodo %d) = %.4f V\n', i, V_completo(i));
end

% Verificar solución
residuo = A_global * V_completo;
fprintf('\nVerificación (A·V debe ser ~0 en nodos interiores):\n');
fprintf('  Residuo en nodos interiores: [%.2e, %.2e, %.2e]\n', ...
        residuo(2), residuo(3), residuo(4));

% =========================================================================
% GRÁFICA DE LA SOLUCIÓN
% =========================================================================

figure('Position', [200, 200, 1000, 400]);

% Gráfica de distribución de potencial
subplot(1, 2, 1);
plot(node_positions, V_completo, 'o-', 'LineWidth', 2.5, 'MarkerSize', 12, ...
     'Color', [0.2, 0.4, 0.8], 'MarkerFaceColor', [1, 0.3, 0.3]);
grid on;
xlabel('Posición (m)', 'FontSize', 12);
ylabel('Potencial V (V)', 'FontSize', 12);
title('Distribución de Potencial en el Dominio', ...
      'FontSize', 13, 'FontWeight', 'bold');

% Añadir valores en los nodos
for i = 1:n_nodos
    text(node_positions(i), V_completo(i) + 0.3, ...
         sprintf('%.2f V', V_completo(i)), ...
         'HorizontalAlignment', 'center', 'FontSize', 9);
end

% Gráfica del campo eléctrico (gradiente de potencial)
subplot(1, 2, 2);
E_field = zeros(n_elementos, 1);
elem_centers = zeros(n_elementos, 1);

for i = 1:n_elementos
    E_field(i) = -(V_completo(i+1) - V_completo(i)) / L_elem;
    elem_centers(i) = (node_positions(i) + node_positions(i+1)) / 2;
end

bar(elem_centers, E_field, 0.8, 'FaceColor', [0.3, 0.7, 0.3], ...
    'EdgeColor', 'k', 'LineWidth', 1.5);
grid on;
xlabel('Posición (m)', 'FontSize', 12);
ylabel('Campo Eléctrico E (V/m)', 'FontSize', 12);
title('Campo Eléctrico en cada Elemento', ...
      'FontSize', 13, 'FontWeight', 'bold');

% Añadir valores sobre barras
for i = 1:n_elementos
    text(elem_centers(i), E_field(i) + 1, ...
         sprintf('%.1f', E_field(i)), ...
         'HorizontalAlignment', 'center', 'FontSize', 9, 'FontWeight', 'bold');
end

sgtitle('Solución del Problema con Condiciones de Frontera', ...
        'FontSize', 14, 'FontWeight', 'bold');

% =========================================================================
% ANÁLISIS DE PROPIEDADES DE LA MATRIZ
% =========================================================================

fprintf('\n============================================================\n');
fprintf('PASO 5: Análisis de Propiedades de la Matriz\n');
fprintf('============================================================\n\n');

% Verificar simetría
es_simetrica = isequal(A_global, A_global');
fprintf('¿Es simétrica?: %s\n', mat2str(es_simetrica));

% Verificar definida positiva
autovalores = eig(A_global);
es_def_positiva = all(autovalores > 0);
fprintf('¿Es definida positiva?: %s\n', mat2str(es_def_positiva));

% Número de condición
cond_number = cond(A_global);
fprintf('Número de condición: %.2e\n', cond_number);

% Sparsity
num_no_ceros = nnz(A_global);
num_total = numel(A_global);
sparsity = (1 - num_no_ceros/num_total) * 100;
fprintf('Sparsity: %.1f%% (solo %.0f%% son no nulos)\n', ...
        sparsity, 100 - sparsity);

fprintf('\nAutovalores de la matriz:\n');
for i = 1:length(autovalores)
    fprintf('  λ_%d = %.4f\n', i, autovalores(i));
end

% =========================================================================
% RESUMEN FINAL
% =========================================================================

fprintf('\n============================================================\n');
fprintf('                  RESUMEN FINAL\n');
fprintf('============================================================\n\n');

fprintf('✅ Método de Elementos Finitos implementado exitosamente\n\n');

fprintf('Características del ensamblaje:\n');
fprintf('  • Matriz global: %d × %d\n', n_nodos, n_nodos);
fprintf('  • Estructura: Tridiagonal (banda = 1)\n');
fprintf('  • Elementos no nulos: %d de %d (%.1f%%)\n', ...
        num_no_ceros, num_total, 100*num_no_ceros/num_total);
fprintf('  • Simetría: %s\n', mat2str(es_simetrica));
fprintf('  • Definida positiva: %s\n\n', mat2str(es_def_positiva));

fprintf('Proceso clave del MEF:\n');
fprintf('  1. Discretizar dominio en elementos\n');
fprintf('  2. Calcular matrices elementales locales\n');
fprintf('  3. Ensamblar sumando contribuciones\n');
fprintf('  4. Aplicar condiciones de frontera\n');
fprintf('  5. Resolver sistema lineal A·V = F\n\n');

fprintf('============================================================\n');
fprintf('              ✓ ANÁLISIS COMPLETADO\n');
fprintf('============================================================\n');