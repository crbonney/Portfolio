clear all;
close all;

im = imread('hw10image.png');
im = single(im);
im = im / max(im(:));

%figure;
%imshow(im);

imdft = fft2(im);
imdft = fftshift(imdft);

[rows, columns, numberOfColorChannels] = size(imdft);

imdft_mag = log(abs(imdft));
imdft_mag = imdft_mag / max(imdft_mag(:));

figure;
imshow(imdft_mag);

ui = 134;
vi = 222;
for n = 0 : 125
    imdft(ui-n, vi) = 1;
    imdft(rows - (ui-n) + 2, columns - vi + 2) = 1;
end
for n = 0 : 200
    imdft(ui+n, vi) = 1;
    imdft(rows - (ui+n) + 2, columns - vi + 2) = 1;
end
for n = 0 : 50
    imdft(ui, vi+n) = 1;
    imdft(rows - ui + 2, columns - (vi+n) + 2) = 1;
end
for n = 0 : 50
    imdft(ui, vi-n) = 1;
    imdft(rows - ui + 2, columns - (vi-n) + 2) = 1;
end

imdft_mag = log(abs(imdft));
imdft_mag = imdft_mag / max(imdft_mag(:));

figure;
imshow(imdft_mag);


imdft = fftshift(imdft);

newim = ifft2(imdft);
figure;
imshow(newim);

imwrite(newim, 'hw10image_filtered.png');