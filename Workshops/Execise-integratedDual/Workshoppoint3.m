% =========================================================================
% MÉTODO DE LOS ELEMENTOS DE FRONTERA (BEM)
% Problema Electrostático: ∇²φ = 0 (Laplace)
% =========================================================================

clear; clc; close all;

fprintf('============================================================\n');
fprintf('  MÉTODO DE ELEMENTOS DE FRONTERA (BEM)\n');
fprintf('  Problema Electrostático: ∇²φ = 0\n');
fprintf('============================================================\n\n');

% =========================================================================
% PASO 1: DEFINICIÓN DE LA GEOMETRÍA
% =========================================================================
fprintf('PASO 1: Definición de la Geometría\n');
fprintf('------------------------------------------------------------\n');

% Definir 5 nodos en la frontera (cuadro cerrado)
nodes = [
    0.0, 0.0;   % Nodo 1
    1.0, 0.0;   % Nodo 2
    1.0, 1.0;   % Nodo 3
    0.0, 1.0;   % Nodo 4
    0.0, 0.0    % Nodo 5 (cierra el contorno)
];

n_nodes = size(nodes, 1);
n_elements = n_nodes - 1;  % 4 elementos

% Conectividad
elements = zeros(n_elements, 2);
for i = 1:n_elements
    elements(i,:) = [i, i+1];
end

fprintf('Número de nodos: %d\n', n_nodes);
fprintf('Número de elementos de frontera: %d\n\n', n_elements);

% Potencial conocido en la frontera (condición de Dirichlet)
phi_boundary = [0; 0; 10; 10; 0];  % Diferentes valores en cada lado

fprintf('Condiciones de frontera (potencial conocido):\n');
for i = 1:n_nodes
    fprintf('  Nodo %d: φ = %.1f V\n', i, phi_boundary(i));
end

% =========================================================================
% PASO 2: FUNCIÓN DE GREEN
% =========================================================================
fprintf('\n============================================================\n');
fprintf('PASO 2: Función de Green\n');
fprintf('============================================================\n\n');

fprintf('Función de Green para 2D:\n');
fprintf('  G(r, r'') = -1/(2π) * ln(|r - r''|)\n\n');

green_function = @(r, r_prime) -log(max(norm(r - r_prime), 1e-10)) / (2*pi);

% =========================================================================
% PASO 3: MATRIZ DE INTERACCIÓN [Z]
% =========================================================================
fprintf('============================================================\n');
fprintf('PASO 3: Construcción de la Matriz [Z]\n');
fprintf('============================================================\n\n');

% Puntos de colocación (centros de los elementos)
collocation_points = zeros(n_elements, 2);
for i = 1:n_elements
    node1 = nodes(elements(i,1), :);
    node2 = nodes(elements(i,2), :);
    collocation_points(i,:) = (node1 + node2) / 2;
end

Z = zeros(n_elements, n_elements);
for m = 1:n_elements
    for n = 1:n_elements
        r_obs = collocation_points(m,:);
        node1 = nodes(elements(n,1), :);
        node2 = nodes(elements(n,2), :);
        length_n = norm(node2 - node1);
        r_source = (node1 + node2) / 2;
        G = green_function(r_obs, r_source);
        Z(m,n) = G * length_n;
    end
end

fprintf('✓ Matriz Z calculada\n');
disp(Z);

% =========================================================================
% PASO 4: VECTOR DEL LADO DERECHO [V]
% =========================================================================
fprintf('============================================================\n');
fprintf('PASO 4: Vector del Lado Derecho [V]\n');
fprintf('============================================================\n\n');

V = zeros(n_elements, 1);
for m = 1:n_elements
    node1_idx = elements(m,1);
    node2_idx = elements(m,2);
    V(m) = (phi_boundary(node1_idx) + phi_boundary(node2_idx)) / 2;
end

fprintf('Vector V:\n');
disp(V);

% =========================================================================
% PASO 5: SOLUCIÓN DEL SISTEMA [Z][C] = [V]
% =========================================================================
fprintf('============================================================\n');
fprintf('PASO 5: Solución del Sistema Lineal\n');
fprintf('============================================================\n\n');

C = Z \ V;
fprintf('Coeficientes de densidad de carga C:\n');
disp(C);

% =========================================================================
% PASO 6: RECONSTRUCCIÓN DEL POTENCIAL
% =========================================================================
fprintf('============================================================\n');
fprintf('PASO 6: Cálculo del Potencial Interno\n');
fprintf('============================================================\n\n');

x_range = linspace(0.05, 0.95, 30);
y_range = linspace(0.05, 0.95, 30);
[X, Y] = meshgrid(x_range, y_range);
phi_internal = zeros(size(X));

for i = 1:size(X, 1)
    for j = 1:size(X, 2)
        r_obs = [X(i,j), Y(i,j)];
        phi_point = 0;
        for n = 1:n_elements
            node1 = nodes(elements(n,1), :);
            node2 = nodes(elements(n,2), :);
            r_source = (node1 + node2)/2;
            length_n = norm(node2 - node1);
            G = green_function(r_obs, r_source);
            phi_point = phi_point + C(n)*G*length_n;
        end
        phi_internal(i,j) = phi_point;
    end
end

fprintf('✓ Potencial calculado en el dominio interno\n');

% =========================================================================
% PASO 7: CÁLCULO DEL CAMPO ELÉCTRICO
% =========================================================================
[Ex, Ey] = gradient(-phi_internal);

% =========================================================================
% VISUALIZACIONES
% =========================================================================
figure('Position',[100 100 1500 800]);

subplot(1,2,1);
hold on; grid on; axis equal;
title('Geometría y elementos de frontera');
for i = 1:n_elements
    node1 = nodes(elements(i,1), :);
    node2 = nodes(elements(i,2), :);
    plot([node1(1), node2(1)], [node1(2), node2(2)], 'b-', 'LineWidth',2);
end
plot(nodes(:,1), nodes(:,2), 'ko','MarkerFaceColor','k');
xlabel('x'); ylabel('y');
text(0.5, -0.1, '0V', 'FontSize',10);
text(1.05, 0.5, '5V', 'FontSize',10);
text(0.5, 1.05, '10V', 'FontSize',10);
text(-0.1, 0.5, '5V', 'FontSize',10);

subplot(1,2,2);
contourf(X, Y, phi_internal, 20, 'LineColor','none');
colorbar; title('Distribución del Potencial φ(x,y)');
xlabel('x'); ylabel('y');
axis equal tight;
hold on;
quiver(X, Y, Ex, Ey, 2, 'k');
title('Potencial y Campo Eléctrico');
