#perl NormalizeMatrix.pl -i loop$1/step5/Q.step5.4x.1
#perl NormalizeMatrix.pl -i loop$1/step5/Q.step5.4x.2
#perl NormalizeMatrix.pl -i loop$1/step5/Q.step5.4x.3
#perl NormalizeMatrix.pl -i loop$1/step5/Q.step5.4x.4
cp loop$1/step5/Q.step5.4x.1 loop$1/step5/Q.step5.4x.1.normalized 
cp loop$1/step5/Q.step5.4x.2 loop$1/step5/Q.step5.4x.2.normalized
cp loop$1/step5/Q.step5.4x.3 loop$1/step5/Q.step5.4x.3.normalized
cp loop$1/step5/Q.step5.4x.4 loop$1/step5/Q.step5.4x.4.normalized
#python Normalize.py loop$1/step5/Q.step5.4x.1 $2
#python Normalize.py loop$1/step5/Q.step5.4x.2 $2
#python Normalize.py loop$1/step5/Q.step5.4x.3 $2
#python Normalize.py loop$1/step5/Q.step5.4x.4 $2
