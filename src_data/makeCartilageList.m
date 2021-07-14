%function compStatus = makeCartilageList(nm)
function tissue = makeCartilageList(nm)
%function tissueProps = makeCartilageList(nm)
%   Returns the tissue optical properties at the wavelength nm:
%       tissueProps = [mua; mus; g]';
%       global tissuenames(i).s
%   Uses 
%       SpectralLIB.mat

%% Load spectral library
%load spectralLIB.mat
load acspectralLIB.mat
%   muasz      381x1     xxxx  double              
%   muamz      381x1     xxxx  double              
%   muadz      381x1     xxxx  double              
%   muac       381x1     xxxx  double                       
%   nmwave     381x1     xxxx  double 

% mus actually musp, so was x10 to take it to mus
MU(:,1) = interp1(nmwave,mua_sz,nm);
MU(:,2) = interp1(nmwave,mus_sz*10,nm); 

MU(:,3) = interp1(nmwave,mua_mz,nm);
MU(:,4) = interp1(nmwave,mus_mz*10,nm);

MU(:,5) = interp1(nmwave,mua_dz,nm);
MU(:,6) = interp1(nmwave,mus_dz*10,nm);

MU(:,7) = interp1(nmwave,mua_c,nm);
MU(:,8) = interp1(nmwave,mus_c*10,nm);

LOADED = 1;

%% Create tissueList

j=1;
tissue(j).name  = 'air';
tissue(j).mua   = 0.0001;     % Negligible absorption yet still tracks, 
tissue(j).mus   = 1.0;        % but take steps in air
tissue(j).g     = 1.0;        % and don't scatter.

j=2;
tissue(j).name  = 'superfic zone';
tissue(j).mua   = MU(1);
tissue(j).mus   = MU(2);      % Take steps in water,
tissue(j).g     = 0.9;        % scatter.

j=3;
tissue(j).name  = 'middle zone';
tissue(j).mua   = MU(3);
tissue(j).mus   = MU(4);      % Take steps in water,
tissue(j).g     = 0.9;        % scatter.

j=4;
tissue(j).name  = 'deep zone';
tissue(j).mua   = MU(5);
tissue(j).mus   = MU(6);      % Take steps in water,
tissue(j).g     = 0.9;        % scatter.

j=5;
tissue(j).name  = 'whole cartilage';
tissue(j).mua   = MU(7);
tissue(j).mus   = MU(8);      % Take steps in water,
tissue(j).g     = 0.9;        % scatter.

% FIX THIS & USE AS SUBCHONDRAL BONE
% j=6;
% tissue(j).name  = 'subchond bone';    % could represent subchondral bone? 
% B = 0.0005;
% S = 0.75;
% W = 0.35;
% M = 0;
% musp500 = 30;
% fray    = 0.0;
% bmie    = 1.0;
% gg      = 0.90;
% musp = musp500*(fray*(nm/500).^-4 + (1-fray)*(nm/500).^-bmie);
% X = [B*S B*(1-S) W M]';
% tissue(j).mua = MU*X;
% tissue(j).mus = musp/(1-gg);
% tissue(j).g   = gg;

j=6;
tissue(j).name  = 'standard tissue';
tissue(j).mua   = 1;
tissue(j).mus   = 100;
tissue(j).g     = 0.90;

disp(sprintf('---- tissueList ------ \tmua   \tmus  \tg  \tmusp'))
for i=1:length(tissue)
    disp(sprintf('%d\t%15s\t%0.4f\t%0.1f\t%0.3f\t%0.1f',...
        i,tissue(i).name, tissue(i).mua,tissue(i).mus,tissue(i).g,...
        tissue(i).mus*(1-tissue(i).g)))
end
compStatus = 1;
disp(' ')

