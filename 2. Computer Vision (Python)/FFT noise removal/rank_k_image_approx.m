clear all
close all

file = 'hw10image_filtered.png';

im = imread(file);
im = single(im);
im = im/max(im(:));

[U,S,V] = svd(im);

k = 50;

im_k = U(:,1:k)*S(1:k,1:k)*V(:,1:k)';

im_k2 = 0.*im;

for i=1:k
  im_k2 = im_k2 + U(:,i)*S(i,i)*V(:,i)';
end
figure
imshow(im);
figure
imshow(im_k);
figure
imshow(im_k2);