# homework

Python implementation of the Data Science Assignment.

Description 
-----------
This project combines multispectral images into a regular RGB colored image. 
As input it takes full spectral resolution reflectance data from 400nm to 700nm at 10nm steps (31 bands total). Each band is stored as a 16-bit grayscale PNG image.
More infromation about the data can be found at http://www1.cs.columbia.edu/CAVE/databases/multispectral/ .

Ideally to obtain RGB values we need to know the whole visible spectrum S(l) for a wavelength l from 400nm to 700nm.
We have estimation of this function at 31 equidistant points l = 400, 410, 420 ... 700.
We approximate S(l) through a piecewise linear function.


To calculate the RGB values we compute the integral of product of the visible spectrum S(l) and the kernels R(l), G(l), B(l) for red, green and blue values correspondingly:

![equation](http://www.sciweavers.org/tex2img.php?eq=R%20%3D%20%5Cint_%7B400%7D%5E%7B700%7D%20S%28l%29%20R%28l%29dl%2C%5Cquad%0AG%20%3D%20%5Cint_%7B400%7D%5E%7B700%7D%20S%28l%29%20G%28l%29dl%2C%5Cquad%0AB%20%3D%20%5Cint_%7B400%7D%5E%7B700%7D%20S%28l%29%20B%28l%29dl%20%0A&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

The kernels were taken from http://stackoverflow.com/questions/3407942/rgb-values-of-visible-spectrum



Requirements
-----
python2.7 <br />
numpy  
scipy  
Pillow

Installation and Usage
-----
Build the latest development version from source:
```
git clone https://github.com/larisahax/homework.git
cd homework/
```

To run in isolated Python environment, use ```virtualenv```.
```
pip install virtualenv
virtualenv --no-site-packages virtual-python
source virtual-python/bin/activate
```
Install the required packages using pip:

```
pip install numpy scipy Pillow
```
Finally run the code:
```
python homework.py
```
This will create an RGB colored image and store it in the working directory as ```answer.png```.
