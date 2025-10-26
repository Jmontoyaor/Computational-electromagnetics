% fem_laplace.m
% Método de Elementos Finitos - Ecuación de Laplace ∇^2 φ = 0 (Dirichlet en y)
clear; clc; close all;

fprintf('============================================================\n');
fprintf('  FEM - Laplace: ∇^2 φ = 0 (Dirichlet en y)\n');
fprintf('============================================================\n\n');

% -----------------------------
% Parámetros de la malla / dominio
% -----------------------------
nx = 6;     % nodos en x (columnas)
ny = 6;     % nodos en y (filas)
Lx = 1.0;   % longitud x
Ly = 1.0;   % longitud y

x = linspace(0, Lx, nx);
y = linspace(0, Ly, ny);
[X, Y] = meshgrid(x, y);

nodes = [X(:), Y(:)];       % N x 2
n_nodes = size(nodes, 1);

% Triangulación regular: 2 triángulos por celda
elements = [];
for j = 1:ny-1
    for i = 1:nx-1
        n1 = (j-1)*nx + i;
        n2 = (j-1)*nx + (i+1);
        n3 = j*nx + (i+1);
        n4 = j*nx + i;
        elements = [elements; n1, n2, n3; n1, n3, n4];
    end
end
n_elements = size(elements, 1);

fprintf('Dominio: %.2f x %.2f, nodos: %d, elementos: %d\n', Lx, Ly, n_nodes, n_elements);

% -----------------------------
% Condiciones de frontera
% -----------------------------
V0 = 10.0;
boundary_bottom = find(abs(nodes(:,2) - 0) < 1e-12);   % y=0
boundary_top    = find(abs(nodes(:,2) - Ly) < 1e-12);  % y=Ly

fprintf('BC: bottom nodes = %d, top nodes = %d\n', numel(boundary_bottom), numel(boundary_top));

% -----------------------------
% Ensamblaje de K global
% -----------------------------
epsilon_r = 1.0;
K_global = sparse(n_nodes, n_nodes);

for e = 1:n_elements
    elem_nodes = elements(e, :);
    elem_coords = nodes(elem_nodes, :);
    [K_elem, Area] = element_stiffness_matrix(elem_coords, epsilon_r);
    % Ensamblaje
    for i = 1:3
        for j = 1:3
            K_global(elem_nodes(i), elem_nodes(j)) = K_global(elem_nodes(i), elem_nodes(j)) + K_elem(i,j);
        end
    end
end

nnz_K = nnz(K_global);
sparsity = 100 * (1 - nnz_K / (n_nodes^2));
fprintf('Matriz global ensamblada. nnz = %d, sparsity = %.2f%%\n', nnz_K, sparsity);

% -----------------------------
% Aplicar condiciones de frontera (Dirichlet directo)
% -----------------------------
b = zeros(n_nodes, 1);
bc_nodes = [boundary_bottom; boundary_top];
bc_values = [zeros(length(boundary_bottom),1); V0*ones(length(boundary_top),1)];

K_mod = K_global;
b_mod = b;
for k = 1:length(bc_nodes)
    node = bc_nodes(k);
    val = bc_values(k);
    K_mod(node, :) = 0;
    K_mod(node, node) = 1;
    b_mod(node) = val;
end
fprintf('Condiciones de Dirichlet aplicadas: %d nodos\n', length(bc_nodes));

% -----------------------------
% Resolver
% -----------------------------
phi = K_mod \ b_mod;
fprintf('Sistema resuelto. phi: min=%.6f, max=%.6f, mean=%.6f\n', min(phi), max(phi), mean(phi));

% -----------------------------
% Calcular campo E = -∇φ por elemento
% -----------------------------
E_field = zeros(n_elements, 2);
elem_centers = zeros(n_elements, 2);
E_mag = zeros(n_elements,1);

for e = 1:n_elements
    elem_nodes = elements(e,:);
    elem_coords = nodes(elem_nodes,:);
    phi_elem = phi(elem_nodes);
    elem_centers(e,:) = mean(elem_coords,1);
    
    % Coeficientes b, c
    x1 = elem_coords(1,1); y1 = elem_coords(1,2);
    x2 = elem_coords(2,1); y2 = elem_coords(2,2);
    x3 = elem_coords(3,1); y3 = elem_coords(3,2);
    Area = 0.5 * abs( (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1) );
    b = [y2 - y3; y3 - y1; y1 - y2];
    c = [x3 - x2; x1 - x3; x2 - x1];
    % grad phi
    dphi_dx = (b' * phi_elem) / (2*Area);
    dphi_dy = (c' * phi_elem) / (2*Area);
    E = -[dphi_dx, dphi_dy];
    E_field(e, :) = E;
    E_mag(e) = norm(E);
end

fprintf('Campo E calculado en %d elementos. |E|: min=%.6e, max=%.6e, mean=%.6e\n', ...
        n_elements, min(E_mag), max(E_mag), mean(E_mag));

% -----------------------------
% Visualizaciones
% -----------------------------
figure('Position',[50 50 1400 900]);

% 1) malla
subplot(2,3,1); hold on;
for e = 1:n_elements
    coords = nodes(elements(e,:),:);
    patch(coords(:,1), coords(:,2), 'w', 'EdgeColor','k');
end
plot(nodes(:,1), nodes(:,2), 'ro','MarkerSize',3);
plot(nodes(boundary_bottom,1), nodes(boundary_bottom,2), 'go','MarkerSize',5);
plot(nodes(boundary_top,1), nodes(boundary_top,2), 'mo','MarkerSize',5);
axis equal tight; grid on; title('Malla');

% 2) contornos de phi
subplot(2,3,2);
phi_grid = reshape(phi, ny, nx);
contourf(X, Y, phi_grid, 20, 'LineColor','none'); colorbar;
axis equal tight; title('Distribución potencial φ');

% 3) superficie phi
subplot(2,3,3);
surf(X, Y, phi_grid, 'EdgeColor','none'); view(45,30); colorbar;
axis tight; title('φ (3D)');

% 4) quiver E (submuestreo)
subplot(2,3,4);
step = max(1, floor(n_elements/100));
quiver(elem_centers(1:step:end,1), elem_centers(1:step:end,2), ...
       E_field(1:step:end,1), E_field(1:step:end,2), 1.5);
axis equal tight; title('Campo E (element centers)'); grid on;

% 5) |E| por elemento (patch)
subplot(2,3,5);
hold on;
for e=1:n_elements
    coords = nodes(elements(e,:),:);
    patch(coords(:,1), coords(:,2), E_mag(e), 'EdgeColor','none');
end
colorbar; axis equal tight; title('|E| por elemento');

% 6) perfil central y linea BC
subplot(2,3,6);
mid_idx = ceil(nx/2);
phi_center = phi_grid(:, mid_idx);
plot(y, phi_center, 'b-o'); hold on;
yline(0,'g--'); yline(V0,'m--'); title(sprintf('φ a lo largo de x=%.2f', x(mid_idx)));
grid on;

sgtitle('Solución FEM de ∇^2 φ = 0');

% -----------------------------
% Comparación con solución analítica (φ = V0 * y / Ly)
% -----------------------------
phi_analytical = V0 * nodes(:,2) / Ly;
error_abs = abs(phi - phi_analytical);
error_rms = sqrt(mean(error_abs.^2));
fprintf('Error RMS frente analítica (φ=V0*y/Ly): %.6e\n', error_rms);

% -----------------------------
% Estudio de convergencia simple
% -----------------------------
mesh_sizes = [4, 6, 8, 10, 12];
errors_convergence = zeros(size(mesh_sizes));
for idx = 1:length(mesh_sizes)
    n = mesh_sizes(idx);
    x_temp = linspace(0,Lx,n); y_temp = linspace(0,Ly,n);
    [X_t, Y_t] = meshgrid(x_temp, y_temp);
    nodes_t = [X_t(:), Y_t(:)];
    % generar elementos
    elements_t = [];
    for j=1:n-1
        for i=1:n-1
            n1 = (j-1)*n + i;
            n2 = (j-1)*n + (i+1);
            n3 = j*n + (i+1);
            n4 = j*n + i;
            elements_t = [elements_t; n1,n2,n3; n1,n3,n4];
        end
    end
    n_nodes_t = size(nodes_t,1); n_e_t = size(elements_t,1);
    Kt = sparse(n_nodes_t, n_nodes_t);
    for e=1:n_e_t
        elem_nodes = elements_t(e,:);
        elem_coords = nodes_t(elem_nodes,:);
        [Ke, ~] = element_stiffness_matrix(elem_coords, epsilon_r);
        for i=1:3
            for j=1:3
                Kt(elem_nodes(i), elem_nodes(j)) = Kt(elem_nodes(i), elem_nodes(j)) + Ke(i,j);
            end
        end
    end
    % BC
    bottom_t = find(abs(nodes_t(:,2)-0)<1e-12);
    top_t = find(abs(nodes_t(:,2)-Ly)<1e-12);
    bc_n = [bottom_t; top_t];
    bc_v = [zeros(length(bottom_t),1); V0*ones(length(top_t),1)];
    bt = zeros(n_nodes_t,1);
    Kt_mod = Kt;
    for k=1:length(bc_n)
        node = bc_n(k);
        Kt_mod(node,:) = 0;
        Kt_mod(node,node)=1;
        bt(node)=bc_v(k);
    end
    phi_t = Kt_mod \ bt;
    phi_anal_t = V0 * nodes_t(:,2) / Ly;
    errors_convergence(idx) = sqrt(mean((phi_t - phi_anal_t).^2));
    fprintf('Mesh %2d x %2d: nodes=%d, elems=%d, errorRMS=%.3e\n', n,n, n_nodes_t, n_e_t, errors_convergence(idx));
end

figure;
loglog(mesh_sizes.^2, errors_convergence, 'o-','LineWidth',2);
xlabel('Número de nodos'); ylabel('Error RMS'); grid on;
title('Convergencia FEM');

% =======================
% Función local: matriz de rigidez elemental (triángulo lineal)
% =======================
function [K_elem, Area] = element_stiffness_matrix(node_coords, epsilon_r)
    x1 = node_coords(1,1); y1 = node_coords(1,2);
    x2 = node_coords(2,1); y2 = node_coords(2,2);
    x3 = node_coords(3,1); y3 = node_coords(3,2);
    Area = 0.5 * abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1));
    b = [y2 - y3; y3 - y1; y1 - y2];
    c = [x3 - x2; x1 - x3; x2 - x1];
    K_elem = zeros(3,3);
    for i=1:3
        for j=1:3
            K_elem(i,j) = epsilon_r * (b(i)*b(j) + c(i)*c(j)) / (4 * Area);
        end
    end
end
