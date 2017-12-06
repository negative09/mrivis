# Autogenerated with SMOP 0.32-7-gcce8558
from smop.core import *
# mrivis_checkerboard.m

    
@function
def mrivis_checkerboard(img_spec1=None,img_spec2=None,patch_size=None,fig_handle=None,rescale_intensity_range=None,varargin=None,*args,**kwargs):
    varargin = mrivis_checkerboard.varargin
    nargin = mrivis_checkerboard.nargin

    # mrivis_collage( img_spec1, img_spec2, fig_handle)
#   img_spec1  = MR image (or path to one) to be visualized
#   img_spec2  = second MR image/path to be compared
#   patch_size = size of patch in checkerboard (default 10 voxels square)
#       This could be rectangular also e.g. [10, 30] specifying width and height of patch.
#   fig_handle = figure handle to display the images
#   scale_intensity_flag - whether to rescale image intensities or not
#       can be a flag ([true]/false)
#       or an array specifying the [ min max ] to which intensities should be rescaled to
#       - This useful for comparison purposes:
#           when images being visualized is exactly what you wanna see and not the rescaled ones
#   varargin: optional text to be displayed
    
    # setting arguments
    if nargin < 3:
        patch_size=matlabarray(cat(10,10))
# mrivis_checkerboard.m:18
    
    if nargin < 4:
        fig_handle=copy(figure)
# mrivis_checkerboard.m:22
    
    if nargin < 5:
        rescale_intensity_range=copy(true)
# mrivis_checkerboard.m:26
    
    img1=get_image(img_spec1)
# mrivis_checkerboard.m:29
    img2=get_image(img_spec2)
# mrivis_checkerboard.m:30
    img_size=size(img1)
# mrivis_checkerboard.m:32
    img_size2=size(img2)
# mrivis_checkerboard.m:33
    if logical_not(isequal(img_size,img_size2)):
        error('size mismatch! Two images to be compared must be of the same size in all dimensions.')
    
    # cropping the images to their extents
    padding=5
# mrivis_checkerboard.m:39
    img1,img2=crop_to_extents(img1,img2,padding,nargout=2)
# mrivis_checkerboard.m:40
    cropped_img_size=size(img1)
# mrivis_checkerboard.m:42
    num_cross_sections_total=24
# mrivis_checkerboard.m:44
    # skipping first and last 3
    num_cs_to_skip=6
# mrivis_checkerboard.m:46
    slices=cellarray([[round(linspace(1,cropped_img_size[1],num_cross_sections_total))],[round(linspace(1,cropped_img_size[2],num_cross_sections_total))],[round(linspace(1,cropped_img_size[3],num_cross_sections_total))]])
# mrivis_checkerboard.m:47
    RescaleImages=copy(true)
# mrivis_checkerboard.m:54
    
    # estimating intensity ranges
    if length(rescale_intensity_range) == 1 and rescale_intensity_range:
        img_intensity_range=matlabarray(cat(min(ravel(img1)),max(ravel(img1))))
# mrivis_checkerboard.m:58
    else:
        if length(rescale_intensity_range) == 2:
            img_intensity_range=copy(rescale_intensity_range)
# mrivis_checkerboard.m:60
        else:
            RescaleImages=copy(false)
# mrivis_checkerboard.m:62
    
    set(0,'CurrentFigure',fig_handle)
    set(fig_handle,'Color','k')
    for dim_index in arange(1,3).reshape(-1):
        slices_this_dim=slices[dim_index](arange(num_cs_to_skip + 1,end() - num_cs_to_skip))
# mrivis_checkerboard.m:69
        for range_index in arange(1,length(slices_this_dim)).reshape(-1):
            # making the axis
            subplot('Position',get_subplot_pos(dim_index,range_index))
            slice1=getdim(img1,dim_index,slices_this_dim[range_index])
# mrivis_checkerboard.m:76
            slice2=getdim(img2,dim_index,slices_this_dim[range_index])
# mrivis_checkerboard.m:77
            checkers=get_checkers(size(slice1),patch_size)
# mrivis_checkerboard.m:80
            mixed=mix_slices(slice1,slice2,checkers)
# mrivis_checkerboard.m:81
            if RescaleImages:
                imagesc(mixed,img_intensity_range)
            else:
                imshow(mixed)
            # adjustments for proper presentation
            colormap('gray')
            axis('off')
            axis('image')
    
    # displaying some annotation text if provided
# good choice would be the location of the input image (for future refwhen image is shared or misplaced!)
    if nargin > 5:
        pos_annot_path_info=matlabarray(cat(0,0.01,1,0.03))
# mrivis_checkerboard.m:100
        subplot('Position',pos_annot_path_info,'Color','k')
        axis('off')
        text(0.05,0.5,varargin[1],'Interpreter','none','Color','g','BackgroundColor','k','fontsize',12,'horizontalAlignment','left')
    
    return
    
if __name__ == '__main__':
    pass
    
    
@function
def get_image(img_spec=None,*args,**kwargs):
    varargin = get_image.varargin
    nargin = get_image.nargin

    # reading in data
    
    if ischar(img_spec):
        img_vol=MRIread(img_spec)
# mrivis_checkerboard.m:114
        if numel(size(img_vol.vol)) != 3:
            error('Input volume is not 3D!')
        img=img_vol.vol
# mrivis_checkerboard.m:118
    else:
        if isreal(img_spec):
            if numel(size(img_spec)) != 3:
                error('Input volume is not 3D!')
            img=copy(img_spec)
# mrivis_checkerboard.m:123
        else:
            display('Invalid input specified!')
            display('Input either a path to image data, or provide 3d Matrix directly.')
    
    return img
    
if __name__ == '__main__':
    pass
    
    
@function
def get_checkers(slice_size=None,patch_size=None,*args,**kwargs):
    varargin = get_checkers.varargin
    nargin = get_checkers.nargin

    # creates checkerboard of a given tile size, filling a given slice
    
    black=zeros(patch_size)
# mrivis_checkerboard.m:134
    white=ones(patch_size)
# mrivis_checkerboard.m:135
    tile=matlabarray(cat([black,white],[white,black]))
# mrivis_checkerboard.m:136
    tile_size=size(tile)
# mrivis_checkerboard.m:137
    # using ceil so we can clip the extra portions
    num_repeats=ceil(slice_size / tile_size)
# mrivis_checkerboard.m:140
    checkers=repmat(tile,num_repeats)
# mrivis_checkerboard.m:141
    collage_size=size(checkers)
# mrivis_checkerboard.m:143
    if any(collage_size > slice_size):
        if collage_size[1] > slice_size[1]:
            checkers[slice_size[1] + 1:end(),:]=[]
# mrivis_checkerboard.m:146
        if collage_size[2] > slice_size[2]:
            checkers[:,slice_size[2] + 1:end()]=[]
# mrivis_checkerboard.m:149
    
    # patch_size, tile_size, slice_size, num_repeats, collage_size, size(checkers)
    
    return checkers
    
if __name__ == '__main__':
    pass
    
    
@function
def mix_slices(slice1=None,slice2=None,checkers=None,*args,**kwargs):
    varargin = mix_slices.varargin
    nargin = mix_slices.nargin

    mixed=copy(slice1)
# mrivis_checkerboard.m:158
    mixed[checkers > 0]=slice2[checkers > 0]
# mrivis_checkerboard.m:159
    return mixed
    
if __name__ == '__main__':
    pass
    
    
@function
def crop_to_extents(img1=None,img2=None,padding=None,*args,**kwargs):
    varargin = crop_to_extents.varargin
    nargin = crop_to_extents.nargin

    beg_coords1,end_coords1=crop_coords(img1,padding,nargout=2)
# mrivis_checkerboard.m:165
    beg_coords2,end_coords2=crop_coords(img2,padding,nargout=2)
# mrivis_checkerboard.m:166
    beg_coords=min(beg_coords1,beg_coords2)
# mrivis_checkerboard.m:168
    end_coords=max(end_coords1,end_coords2)
# mrivis_checkerboard.m:169
    img1=crop_3dimage(img1,beg_coords,end_coords)
# mrivis_checkerboard.m:171
    img2=crop_3dimage(img2,beg_coords,end_coords)
# mrivis_checkerboard.m:172
    return img1,img2
    
if __name__ == '__main__':
    pass
    
    
@function
def crop_coords(img=None,padding=None,*args,**kwargs):
    varargin = crop_coords.varargin
    nargin = crop_coords.nargin

    coords(arange(),1),coords[:,2],coords[:,3]=ind2sub(size(img),find(img > 0),nargout=3)
# mrivis_checkerboard.m:178
    beg_coords=max(1,min(coords) - padding)
# mrivis_checkerboard.m:179
    end_coords=min(size(img),max(coords) + padding)
# mrivis_checkerboard.m:180
    return beg_coords,end_coords
    
if __name__ == '__main__':
    pass
    
    
@function
def crop_3dimage(img=None,beg_coords=None,end_coords=None,*args,**kwargs):
    varargin = crop_3dimage.varargin
    nargin = crop_3dimage.nargin

    cropped_img=img[beg_coords[1]:end_coords[1],beg_coords[2]:end_coords[2],beg_coords[3]:end_coords[3]]
# mrivis_checkerboard.m:187
    return cropped_img
    
if __name__ == '__main__':
    pass
    
    
@function
def get_subplot_pos(dim_index=None,range_index=None,*args,**kwargs):
    varargin = get_subplot_pos.varargin
    nargin = get_subplot_pos.nargin

    # to identify the positions of the different subplots
    
    if range_index <= 6:
        designated_base=matlabarray(cat([0,0.0],[0,0.33],[0,0.66]))
# mrivis_checkerboard.m:199
    else:
        designated_base=matlabarray(cat([0,0.16],[0,0.49],[0,0.825]))
# mrivis_checkerboard.m:201
    
    base=designated_base[dim_index,:]
# mrivis_checkerboard.m:204
    # bounding box (BB) params for a sequential 6x1 grid
    wBB=0.16
# mrivis_checkerboard.m:207
    hBB=0.155
# mrivis_checkerboard.m:208
    #-# Pattern: [ 1 2 3 4 5 6]
    w=dot(mod(range_index - 1,6),wBB)
# mrivis_checkerboard.m:211
    h=0
# mrivis_checkerboard.m:212
    pos=matlabarray(cat(base + cat(w,h),wBB,hBB - 0.005))
# mrivis_checkerboard.m:213
    return pos
    
if __name__ == '__main__':
    pass
    
    
@function
def get_subplot_pos_quad(dim_index=None,range_index=None,*args,**kwargs):
    varargin = get_subplot_pos_quad.varargin
    nargin = get_subplot_pos_quad.nargin

    # to identify the positions of the different subplots
    
    designated_base=matlabarray(cat([0,0],[0.5,0.535],[0,0.535]))
# mrivis_checkerboard.m:220
    base=designated_base[dim_index,:]
# mrivis_checkerboard.m:221
    # bounding box params for a 4-quad 3x3 grid
    wBB=0.16
# mrivis_checkerboard.m:223
    hBB=0.155
# mrivis_checkerboard.m:223
    #-# Pattern: [ 1 2 3; 4 5 6; 7 8 9]
    w=dot(mod(range_index - 2,3),wBB)
# mrivis_checkerboard.m:225
    h=dot(abs(floor((range_index - 2) / 3) - 2),hBB)
# mrivis_checkerboard.m:226
    pos=matlabarray(cat(base + cat(w,h),wBB,hBB - 0.005))
# mrivis_checkerboard.m:227
    return pos
    
if __name__ == '__main__':
    pass
    