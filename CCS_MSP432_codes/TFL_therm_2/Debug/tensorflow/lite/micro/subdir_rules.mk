################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Each subdirectory must supply rules for building sources it contributes
tensorflow/lite/micro/%.o: ../tensorflow/lite/micro/%.cc $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: GNU Compiler'
	"/Applications/ti/ccs1220/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/bin/arm-none-eabi-gcc-9.2.1" -c -mcpu=cortex-m4 -march=armv7e-m -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -fno-exceptions -DNDEBUG -DTF_LITE_STATIC_MEMORY -DCMSIS_NN -DCMSIS_DEVICE_ARM_CORTEX_M_XX_HEADER_FILE=\"ARMCM4_FP.h\" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/Debug" -I"/Users/rmc0mputer/ti/simplelink_msp432p4_sdk_3_40_01_02/source" -I"/Users/rmc0mputer/ti/simplelink_msp432p4_sdk_3_40_01_02/kernel/nortos" -I"/Users/rmc0mputer/ti/simplelink_msp432p4_sdk_3_40_01_02/kernel/nortos/posix" -I"/Applications/ti/ccs1220/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/arm-none-eabi/include/newlib-nano" -I"/Applications/ti/ccs1220/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/arm-none-eabi/include" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/third_party/kissfft" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/third_party/gemmlowp" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/third_party/flatbuffers/include" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/third_party/ruy" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/hello_world" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/third_party/cmsis" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/third_party/cmsis/CMSIS/Core/Include" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/third_party/cmsis/CMSIS/DSP/Include" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/third_party/cmsis/CMSIS/NN/Include" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/third_party/cmsis/Device/ARM/ARMCM4/Include" -I"/Users/rmc0mputer/ti/simplelink_msp432p4_sdk_3_40_01_02/source/third_party/CMSIS/Include" -Os -ffunction-sections -fdata-sections -g -gdwarf-3 -gstrict-dwarf -Wall -flto -fno-strict-aliasing -MMD -MP -MF"tensorflow/lite/micro/$(basename $(<F)).d_raw" -MT"$(@)" -I"/Users/rmc0mputer/PycharmProjects/Thesis_sat_ML/CCS_MSP432_codes/TFL_therm_2/Debug/syscfg" -std=c++11 -fno-rtti -fno-threadsafe-statics $(GEN_OPTS__FLAG) -o"$@" "$<"
	@echo 'Finished building: "$<"'
	@echo ' '


