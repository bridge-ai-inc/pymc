function status = lookfluence(nm, tissueName) 


home
clc
format compact


SAVEPICSON = 1;
if SAVEPICSON
    sz = 10; fz = 7; fz2 = 9; % to use savepic.m
else
    sz = 12; fz = 9; fz2 = 7; % for screen display
end

%%%% USER CHOICES <---------- you must specify -----
% Parse in as function input
%%%%

% Load header file
filename = sprintf('%s_H.mci',tissueName);
fid = fopen(filename, 'r');
A = fscanf(fid,'%f',[1 Inf])';
fclose(fid);

%% parameters
time_min = A(1);
Nx = A(2);
Ny = A(3);
Nz = A(4);
dx = A(5);
dy = A(6);
dz = A(7);
mcflag = A(8);
launchflag = A(9);
boundaryflag = A(10);
xs = A(11);
ys = A(12);
zs = A(13);
xfocus = A(14);
yfocus = A(15);
zfocus = A(16);
ux0 = A(17);
uy0 = A(18);
uz0 = A(19);
radius = A(20);
waist = A(21);
Nt = A(22);
j = 22;
for i=1:Nt
    j=j+1;
    muav(i,1) = A(j);
    j=j+1;
    musv(i,1) = A(j);
    j=j+1;
    gv(i,1) = A(j);
end

reportHmci(tissueName)

%% Load Fluence rate F(y,x,z) 
filename = sprintf('%s_F.bin',tissueName);
tic
    fid = fopen(filename, 'rb');
    [Data count] = fread(fid, Ny*Nx*Nz, 'float');
    fclose(fid);
toc
F = reshape(Data,Ny,Nx,Nz); % F(y,x,z)

% Load tissue structure in voxels, T(y,x,z) 
filename = sprintf('%s_T.bin',tissueName);
disp(['loading ' filename])
tic
    fid = fopen(filename, 'rb');
    [Data count] = fread(fid, Ny*Nx*Nz, 'uint8');
    fclose(fid);
toc
T = reshape(Data,Ny,Nx,Nz); % T(y,x,z)

clear Data

%%
x = ([1:Nx]-Nx/2-1/2)*dx;
y = ([1:Ny]-Ny/2-1/2)*dx;
z = ([1:Nz]-1/2)*dz;
ux = [2:Nx-1];
uy = [2:Ny-1];
uz = [2:Nz-1];
zmin = min(z);
zmax = max(z);
zdiff = (zmax-zmin);
xmin = min(x);
xmax = max(x);
xdiff = (xmax-xmin);


%% Look at Fluence Fzx @ launch point
Fzx = reshape(F(Ny/2,:,:),Nx,Nz)'; % in z,x plane through source

figure(2);clf
fig = imagesc(x,z,log10(Fzx),[0 1.0])
% fig = imagesc(x,z,log10(Fzx),[.5 2.8])
hold on
text(max(x)*1.2,min(z)-0.04*max(z),'log_{10}( \phi )','fontsize',fz)
colorbar
set(gca,'fontsize',sz)
xlabel('x [mm]')
ylabel('z [mm]')
title('Fluence \phi [W/mm^2/W.delivered] ','fontweight','normal','fontsize',fz)
colormap(makec2f)
axis equal image
%axis([min(x) max(x) min(z) max(z)])
text(min(x)-0.2*max(x),min(z)-0.08*max(z),sprintf('runtime = %0.1f min',time_min),...
    'fontsize',fz2)

if SAVEPICSON
    name = sprintf('%s_Fzx.jpg',tissueName);
    %savepic(2,[4 3],name)
    saveas(fig,name)
end



%% look Azx
Fzx = reshape(F(Ny/2,:,:),Nx,Nz)'; % in z,x plane through source
mua = muav(reshape(T(Ny/2,:,:),Nx,Nz)');
Azx = Fzx.*mua;

figure(4);clf
fig = imagesc(x,z,log10(Azx))
hold on
text(max(x)*1.2,min(z)-0.04*max(z),'log_{10}( A )','fontsize',fz)
colorbar
set(gca,'fontsize',sz)
xlabel('x [mm]')
ylabel('z [mm]')
title('Deposition A [W/mm^3/W.delivered] ','fontweight','normal','fontsize',fz)
colormap(makec2f)
axis equal image
%axis([min(x) max(x) min(z) max(z)])
text(min(x)-0.2*max(x),min(z)-0.08*max(z),sprintf('runtime = %0.1f min',time_min),...
    'fontsize',fz2)

if SAVEPICSON
    name = sprintf('%s_Azx.jpg',tissueName);
    %savepic(2,[4 3],name)
    saveas(fig,name)
end


%% look Fzy
Fzy = reshape(F(:,Nx/2,:),Ny,Nz)';

iy = round((dy*Ny/2 + 0.15)/dy);
iz = round(zs/dz);
zzs  = zs;
%Fdet = mean(reshape(Fzy(iz+[-1:1],iy+[0 1]),6,1));

figure(3);clf
% fig = imagesc(y,z,log10(Fzy),[.5 2.8])
fig = imagesc(y,z,log10(Fzy),[0 6.2])
hold on
text(max(x)*1.2,min(z)-0.04*max(z),'log_{10}( \phi )','fontsize',fz)
colorbar
set(gca,'fontsize',sz)
xlabel('y [mm]')
ylabel('z [mm]')
title('Fluence \phi [W/mm^2/W.delivered] ','fontweight','normal','fontsize',fz)
colormap(makec2f)
axis equal image
text(min(x)-0.2*max(x),min(z)-0.08*max(z),sprintf('runtime = %0.1f min',time_min),...
    'fontsize',fz2)

if SAVEPICSON
    name = sprintf('%s_Fzy.jpg',tissueName);
    %savepic(3,[4 3],name)
    saveas(fig,name)
end


drawnow
status = 1;
disp('done')


