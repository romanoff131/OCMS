%x = [1, 0, 0, 1, 1];
%y = [1, 1, 0, 1, 0];
x = [1,0,1,0,0];
y = [1,0,1,0,1];

% Массивы для хранения оригинальной и сдвинутой последовательностей
original = zeros(1, 20);
shifted = zeros(1, 20);

% Заполнение массива результатов операции XOR и сохранение оригинала
for i = 1:20
    original(i) = xor(x(5), y(5));
    shifted(i) = xor(x(5), y(5));

    sumx = xor(x(1), x(3));
    x = [sumx, x(1:4)];

    sumy = xor(y(2), y(4));
    y = [sumy, y(1:4)];
end

% Вывод заголовка таблицы
fprintf('Сдвиг |                    Биты                   | Автокорреляция\n');

corr = xcorr(original, 'coeff');
% Вывод строк таблицы

figure;
plot(corr);

for shift = 0:20
    fprintf('%5d | ', shift);

    % Вывод битов оригинала
    for i = 1:20
        fprintf('%d', shifted(i));
    end

    fprintf(' | ');

    % Используйте abs для избежания ошибки выхода за пределы массива
    autocorr_value = corr(abs(length(original) - shift) + 1);

    fprintf('%+1.3f\n', autocorr_value);

    % Сдвиг массива
    shifted = [shifted(end), shifted(1:end-1)];
end