import os
import sys


files_to_m = ['100.txt', '1000.txt', '1001.txt', '104.txt', '111.txt', '112.txt', '113.txt', '119.txt', '120.txt', '121.txt', '123.txt', '127.txt', '128.txt', '134.txt', '135.txt', '150.txt', '156.txt', '181.txt', '2.txt', '205.txt', '210.txt', '216.txt', '220.txt', '222.txt', '250.txt', '26.txt', '261.txt', '270.txt', '277.txt', '278.txt', '282.txt', '283.txt', '285.txt', '289.txt', '29.txt', '290.txt', '292.txt', '293.txt', '294.txt', '295.txt', '296.txt', '297.txt', '299.txt', '3.txt', '300.txt', '306.txt', '313.txt', '314.txt', '315.txt', '318.txt', '320.txt', '323.txt', '325.txt', '326.txt', '328.txt', '329.txt', '333.txt', '342.txt', '358.txt', '409.txt', '414.txt', '418.txt', '420.txt', '450.txt', '452.txt', '453.txt', '466.txt', '472.txt', '482.txt', '483.txt', '484.txt', '485.txt', '486.txt', '487.txt', '488.txt', '490.txt', '497.txt', '499.txt', '500.txt', '501.txt', '509.txt', '520.txt', '528.txt', '530.txt', '542.txt', '554.txt', '556.txt', '59.txt', '62.txt', '633.txt', '639.txt', '640.txt', '67.txt', '670.txt', '674.txt', '677.txt', '678.txt', '683.txt', '685.txt', '686.txt', '70.txt', '704.txt', '705.txt', '706.txt', '707.txt', '708.txt', '71.txt', '711.txt', '712.txt', '713.txt', '715.txt', '716.txt', '718.txt', '719.txt', '720.txt', '722.txt', '724.txt', '725.txt', '727.txt', '728.txt', '729.txt', '730.txt', '731.txt', '733.txt', '738.txt', '740.txt', '741.txt', '742.txt', '744.txt', '745.txt', '746.txt', '748.txt', '749.txt', '75.txt', '751.txt', '773.txt', '79.txt', '797.txt', '80.txt', '802.txt', '803.txt', '81.txt', '82.txt', '84.txt', '840.txt', '85.txt', '859.txt', '87.txt', '89.txt', '92.txt', '924.txt', '925.txt', '927.txt', '93.txt', '94.txt', '95.txt', '968.txt', '974.txt', '981.txt', '983.txt', '986.txt', '99.txt']



files = os.listdir("test_data/")

for f in files:
    if f in files_to_m:
        os.rename("test_data/"+f ,"confusion/"+f)
