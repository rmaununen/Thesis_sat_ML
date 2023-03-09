################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
SYSCFG_SRCS += \
../hello_world/hello_world.syscfg 

LDS_SRCS += \
../hello_world/MSP_EXP432P401R_NoRTOS.lds 

CC_SRCS += \
../hello_world/constants.cc \
../hello_world/hello_world_model_data.cc \
../hello_world/main.cc \
../hello_world/main_functions.cc \
../hello_world/output_handler.cc 

C_SRCS += \
../hello_world/hello_world.c \
./syscfg/ti_drivers_config.c \
../hello_world/main_nortos.c 

GEN_FILES += \
./syscfg/ti_drivers_config.c 

GEN_MISC_DIRS += \
./syscfg/ 

C_DEPS += \
./hello_world/hello_world.d \
./syscfg/ti_drivers_config.d \
./hello_world/main_nortos.d 

CC_DEPS += \
./hello_world/constants.d \
./hello_world/hello_world_model_data.d \
./hello_world/main.d \
./hello_world/main_functions.d \
./hello_world/output_handler.d 

OBJS += \
./hello_world/constants.o \
./hello_world/hello_world.o \
./syscfg/ti_drivers_config.o \
./hello_world/hello_world_model_data.o \
./hello_world/main.o \
./hello_world/main_functions.o \
./hello_world/main_nortos.o \
./hello_world/output_handler.o 

GEN_MISC_FILES += \
./syscfg/ti_drivers_config.h \
./syscfg/syscfg_c.rov.xs 

GEN_MISC_DIRS__QUOTED += \
"syscfg/" 

CC_DEPS__QUOTED += \
"hello_world/constants.d" \
"hello_world/hello_world_model_data.d" \
"hello_world/main.d" \
"hello_world/main_functions.d" \
"hello_world/output_handler.d" 

OBJS__QUOTED += \
"hello_world/constants.o" \
"hello_world/hello_world.o" \
"syscfg/ti_drivers_config.o" \
"hello_world/hello_world_model_data.o" \
"hello_world/main.o" \
"hello_world/main_functions.o" \
"hello_world/main_nortos.o" \
"hello_world/output_handler.o" 

GEN_MISC_FILES__QUOTED += \
"syscfg/ti_drivers_config.h" \
"syscfg/syscfg_c.rov.xs" 

C_DEPS__QUOTED += \
"hello_world/hello_world.d" \
"syscfg/ti_drivers_config.d" \
"hello_world/main_nortos.d" 

GEN_FILES__QUOTED += \
"syscfg/ti_drivers_config.c" 

CC_SRCS__QUOTED += \
"../hello_world/constants.cc" \
"../hello_world/hello_world_model_data.cc" \
"../hello_world/main.cc" \
"../hello_world/main_functions.cc" \
"../hello_world/output_handler.cc" 

C_SRCS__QUOTED += \
"../hello_world/hello_world.c" \
"./syscfg/ti_drivers_config.c" \
"../hello_world/main_nortos.c" 

SYSCFG_SRCS__QUOTED += \
"../hello_world/hello_world.syscfg" 


