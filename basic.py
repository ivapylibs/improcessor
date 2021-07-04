#=========================== improcessor_basic ===========================
#
# @class        improcessor.basic
#
# @brief        A generic class that simplifies applying basic image
#               processing to an image.  
#
#
# The basic idea is the ability to specify a series of image processing
# functions in order to convert it from one image representation to
# another like a sequential chain of signal processing operations
#
# Basic manipulations include scaling, clipping, normalization, and
# resizing.  What to do is specified by the arguments of the initial
# function call.  If the arguments are empty, then it will do nothing.
# The order of the arguments makes a difference operationally, as
# improcessor will perform the processing in precisely that order.
#
# The arguments should be passed in pairs as technique/function name
# then optional arguments (this must be a FIX:CELL OBJECT).  It is assumed
# that the processing will function as follows: 
#
# > newimage = technique(image, optargs{:});
#
# FIXME, IS A TUPLE WHAT WOULD BE USED? HOW TO EXPAND ARGUMENTS IN CALL?
#
#
# If there are no optional arguments, then pass an empty cell (this
# works for the built-in options, but may not work for Matlab
# functions).  Possible functions are any function that Matlab has
# satifying the above implementation.  Some built-in options are:
#
#    function newimage = clip(image, [minlimit maxlimit]);
#    function newimage = normalize(image);
#    function newimage = scale(image, [minval maxval]);
#    function newimage = scaleabout(image, [anchorval diameter]);
#
#
#  IMPLEMENTATION:
#
# ```
#  improc = improcessor.basic(options);
#
#  ...
#
#  newImage = improc.apply(Image);
#
#  ...
# ```
#
#  EXAMPLES:
#
#  To upsample an image by a factor of two using bilinear interpolation,
#  one would initialize as:
#
#  improcessor = improcessor.basic('imresize',{2,'bilinear'});
# FIX TO BE PYTHON CORRECT.
#
#  To additionally clip the values to lie between 2 and 20 one would
#  modify the initialization to be:
#
#  improcessor = improcessor_basic('imresize',{2,'bilinear'},'clip',{[2 20]});
# FIX TO BE PYTHON CORRECT.
#
#=========================== improcessor.basic ===========================

#
# @file     basic.py
#
# @author   Patricio A. Vela, pvela@gatech.edu
#
# @date     2021/07/03 [created]
#
#
#=========================== improcessor.basic ===========================

# @classf improcessor
class basic(object)


  def __init__(self,*args)

    self.args = args
    self.ignore_undef = false      #< Ignore undefined functions?

    self.processSequence()


  # FIX: NEEDS TO BE PROTECTED MEMBER FUNCTION
  def processSequence(self)

    # FIX: DEFINITELY NOT CORRECT. DON'T KNOW HOW TO WORK WITH TUPLES.

    lasti = len(self.args)
    ind = 1;

    while (ind <= lasti)
      if isa(varargin{ind},'function_handle')
        numfuncs = numfuncs+1;
        methods{numfuncs} = {func2str(self.args{ind}), self.args{ind+1}};
      else
        switch varargin{ind}
          case {'clip','scale','scaleabout'}
            numfuncs = numfuncs+1;
            methods{numfuncs} = {['builtin_' self.args{ind}], 
                                             self.args{ind+1}};
          case 'normalize'
            numfuncs = numfuncs+1;
            methods{numfuncs} = {'builtin_normalize', {}};
          otherwise,
            if ismember(exist(varargin{ind}), [2 3 5 6]) 
              numfuncs = numfuncs+1;
              methods{numfuncs} = {varargin{ind}, varargin{ind+1}};
            elseif (~ignore_undef)
              disp(['Unknown option (' varargin{ind} '), ignoring']);
            end
        end
      end

      ind = ind+2;

    self.args = args;


  #================================ set ================================
  #
  # @brief  Set parameters/member variables of the improcessor.
  #
  def set(self, fname, varargin)
  # FIX: CHange to *args.

    switch (fname)
      case 'ignore'
        self.ignore_undef = varargin{1}
      case 'processing'
        self.args = args
        self.processSequence()

  #================================ get ================================
  #
  # @brief  Get parameters/member variables of the improcessor.
  #
  def fval = basic_get(fname, varargin)

  switch (fname)
    case 'ignore'
      fval = self.ignore_undef
    case 'processing'
      fval = self.methods



  #=============================== apply ===============================
  #
  # @brief  Execute the image processing sequence.
  #
  # @param[in]  image   The image to process.
  # @param[out] imout   The processed image.
  
  function imout = apply(image)
  
    if (isempty(image) || self.numfuncs == 0) #FIX: equal test?
      imout = []
      return
  
    if (self.numfuncs > 0)
      for ii = 1:numfuncs
        if (isempty(methods{ii}{2}))
          image = feval(methods{ii}{1}, image)
        else
          image = feval(methods{ii}{1}, image, methods{ii}{2}{:})


  #================================ post ===============================
  #
  # @brief  Execute post-processing of given image.
  #
  # @param[in]  image   The image to process.
  # @param[out] imout   The processed image.
  
  def image = post(image)

    # Default is to do nothing. Overload to get less "basic."



# FIX:
# NOT SURE HOW TO INCLUDE.  ARE THESE INTERNALLY AVAILABLE FUNCTIONS
# OUTSIDE OF THE CLASS?

#============================= builtin_clip ============================
#
def nimg = builtin_clip(img, limits)

  nimg = min(max(img, limits(1)), limits(2));


#========================== builtin_normalize ==========================
#
def nimg = builtin_normalize(img, empty)

  minI = min(img(:));
  nimg = (img-minI)/(max(img(:))-minI);


#============================ builtin_scale ============================
#
def nimg = builtin_scale(img, scparms)

  minI = min(img(:));
  nimg = (scparms(2)-scparms(1))*(img-minI)/(max(img(:))-minI) + scparms(1);

#========================== builtin_scaleabout =========================
#
def nimg = builtin_scaleabout(img, scparms)

  minI = min(img(:));
  nimg = scparms(2)*(img-minI)/(max(img(:))-minI) + scparms(1) - scparms(2)/2;

