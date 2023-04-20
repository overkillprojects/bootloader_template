/* Linker script to configure memory regions.
 * It references following symbols, which must be defined in code:
 *   Reset_Handler : Entry of reset handler
 *
 * It defines following symbols, which code can use without definition:
 *   __exidx_start
 *   __exidx_end
 *   __etext
 *   __data_start__
 *   __preinit_array_start
 *   __preinit_array_end
 *   __init_array_start
 *   __init_array_end
 *   __fini_array_start
 *   __fini_array_end
 *   __data_end__
 *   __bss_start__
 *   __bss_end__
 *   __end__
 *   end
 *   __HeapBase
 *   __HeapLimit
 *   __StackLimit
 *   __StackTop
 *   __stack
 */

SEARCH_DIR(.)
GROUP(-lgcc -lc -lnosys)

/*
MEMORY
{
  FLASH (rx) : ORIGIN = 0x27000, LENGTH = 0xc9000
  RAM (rwx) :  ORIGIN = 0x20005000, LENGTH = 0x3b000
  RAM0 (rwx) : ORIGIN = 0x20000000, LENGTH = 0x2000
  RAM1 (rwx) : ORIGIN = 0x20002000, LENGTH = 0x2000
  RAM2 (rwx) : ORIGIN = 0x20004000, LENGTH = 0x2000
  RAM3 (rwx) : ORIGIN = 0x20006000, LENGTH = 0x2000
  RAM4 (rwx) : ORIGIN = 0x20008000, LENGTH = 0x2000
  RAM5 (rwx) : ORIGIN = 0x2000A000, LENGTH = 0x2000
  RAM6 (rwx) : ORIGIN = 0x2000C000, LENGTH = 0x2000
  RAM7 (rwx) : ORIGIN = 0x2000E000, LENGTH = 0x2000
  RAM8 (rwx) : ORIGIN = 0x20010000, LENGTH = 0x30000
  uicr_bootloader_start_address (r) : ORIGIN = 0x10001014, LENGTH = 0x4
}
*/
MEMORY
{
  FLASH (rx) : ORIGIN = 0x27000, LENGTH = 0xc9000
  RAM (rwx) :  ORIGIN = 0x20005000, LENGTH = 0x3b000
  uicr_bootloader_start_address (r) : ORIGIN = 0x10001014, LENGTH = 0x4
}
/*
OUTPUT_FORMAT ("elf32-littlearm", "elf32-bigarm", "elf32-littlearm")

ENTRY(Reset_Handler)

SECTIONS
{
    .text :
    {
        KEEP(*(.isr_vector))
        *(.text*)

        KEEP(*(.init))
        KEEP(*(.fini))

        *crtbegin.o(.ctors)
        *crtbegin?.o(.ctors)
        *(EXCLUDE_FILE(*crtend?.o *crtend.o) .ctors)
        *(SORT(.ctors.*))
        *(.ctors)

        *crtbegin.o(.dtors)
        *crtbegin?.o(.dtors)
        *(EXCLUDE_FILE(*crtend?.o *crtend.o) .dtors)
        *(SORT(.dtors.*))
        *(.dtors)

        *(.rodata*)

        KEEP(*(.eh_frame*))
    } > FLASH

    .ARM.extab :
    {
        *(.ARM.extab* .gnu.linkonce.armextab.*)
    } > FLASH

    __exidx_start = .;
    .ARM.exidx :
    {
        *(.ARM.exidx* .gnu.linkonce.armexidx.*)
    } > FLASH
    __exidx_end = .;

    . = ALIGN(4);
    __etext = .;

    .data : AT (__etext)
    {
        __data_start__ = .;
        *(vtable)
        *(.data*)

        . = ALIGN(4);
        PROVIDE_HIDDEN (__preinit_array_start = .);
        KEEP(*(.preinit_array))
        PROVIDE_HIDDEN (__preinit_array_end = .);

        . = ALIGN(4);
        PROVIDE_HIDDEN (__init_array_start = .);
        KEEP(*(SORT(.init_array.*)))
        KEEP(*(.init_array))
        PROVIDE_HIDDEN (__init_array_end = .);


        . = ALIGN(4);
        PROVIDE_HIDDEN (__fini_array_start = .);
        KEEP(*(SORT(.fini_array.*)))
        KEEP(*(.fini_array))
        PROVIDE_HIDDEN (__fini_array_end = .);

        KEEP(*(.jcr*))
        . = ALIGN(4);
        __data_end__ = .;

    } > RAM

    .bss :
    {
        . = ALIGN(4);
        __bss_start__ = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        __bss_end__ = .;
    } > RAM
    
    .heap (COPY):
    {
        __HeapBase = .;
        __end__ = .;
        PROVIDE(end = .);
        KEEP(*(.heap*))
        __HeapLimit = .;
    } > RAM

    .stack_dummy (COPY):
    {
        KEEP(*(.stack*))
    } > RAM

    __StackTop = ORIGIN(RAM) + LENGTH(RAM);
    __StackLimit = __StackTop - SIZEOF(.stack_dummy);
    PROVIDE(__stack = __StackTop);

    ASSERT(__StackLimit >= __HeapLimit, "region RAM overflowed with stack")
    
    DataInitFlashUsed = __bss_start__ - __data_start__;
    CodeFlashUsed = __etext - ORIGIN(FLASH);
    TotalFlashUsed = CodeFlashUsed + DataInitFlashUsed;
    ASSERT(TotalFlashUsed <= LENGTH(FLASH), "region FLASH overflowed with .data and user data")
    
}
*/
/*
SECTIONS
{
  .bss :
  {
      . = ALIGN(4);
      __bss_start__ = .;
      *(.bss*)
      *(COMMON)
      . = ALIGN(4);
      __bss_end__ = .;
  } > RAM8
}
*/

SECTIONS
{
  . = ALIGN(4);
  .uicr_bootloader_start_address :
  {
    PROVIDE(__start_uicr_bootloader_start_address = .);
    KEEP(*(SORT(.uicr_bootloader_start_address*)))
    PROVIDE(__stop_uicr_bootloader_start_address = .);
  } > uicr_bootloader_start_address
/*
  .file_buffer_1 :
  {
    KEEP(*(.file_buffer_1))
  } > RAM6
  
  .file_buffer_0 :
  {
    KEEP(*(.file_buffer_0))
  } >RAM7
  
  .flash_tx_buffer :
  {
    KEEP(*(.flash_tx_buffer))
  } > RAM5
  */
  /*
  .pwm_arrays :
  {
    KEEP(*(.pwm_arrays))
  } > RAM8
  */
}


SECTIONS
{
  . = ALIGN(4);
  .mem_section_dummy_ram :
  {
  }
  .log_dynamic_data :
  {
    PROVIDE(__start_log_dynamic_data = .);
    KEEP(*(SORT(.log_dynamic_data*)))
    PROVIDE(__stop_log_dynamic_data = .);
  } > RAM
  .log_filter_data :
  {
    PROVIDE(__start_log_filter_data = .);
    KEEP(*(SORT(.log_filter_data*)))
    PROVIDE(__stop_log_filter_data = .);
  } > RAM
  .fs_data :
  {
    PROVIDE(__start_fs_data = .);
    KEEP(*(.fs_data))
    PROVIDE(__stop_fs_data = .);
  } > RAM
} INSERT AFTER .data;

SECTIONS
{
  .mem_section_dummy_rom :
  {
  }
  .sdh_ble_observers :
  {
    PROVIDE(__start_sdh_ble_observers = .);
    KEEP(*(SORT(.sdh_ble_observers*)))
    PROVIDE(__stop_sdh_ble_observers = .);
  } > FLASH
  .sdh_soc_observers :
  {
    PROVIDE(__start_sdh_soc_observers = .);
    KEEP(*(SORT(.sdh_soc_observers*)))
    PROVIDE(__stop_sdh_soc_observers = .);
  } > FLASH
  .pwr_mgmt_data :
  {
    PROVIDE(__start_pwr_mgmt_data = .);
    KEEP(*(SORT(.pwr_mgmt_data*)))
    PROVIDE(__stop_pwr_mgmt_data = .);
  } > FLASH
  .log_const_data :
  {
    PROVIDE(__start_log_const_data = .);
    KEEP(*(SORT(.log_const_data*)))
    PROVIDE(__stop_log_const_data = .);
  } > FLASH
  .sdh_req_observers :
  {
    PROVIDE(__start_sdh_req_observers = .);
    KEEP(*(SORT(.sdh_req_observers*)))
    PROVIDE(__stop_sdh_req_observers = .);
  } > FLASH
  .sdh_state_observers :
  {
    PROVIDE(__start_sdh_state_observers = .);
    KEEP(*(SORT(.sdh_state_observers*)))
    PROVIDE(__stop_sdh_state_observers = .);
  } > FLASH
  .sdh_stack_observers :
  {
    PROVIDE(__start_sdh_stack_observers = .);
    KEEP(*(SORT(.sdh_stack_observers*)))
    PROVIDE(__stop_sdh_stack_observers = .);
  } > FLASH
  .log_backends :
  {
    PROVIDE(__start_log_backends = .);
    KEEP(*(SORT(.log_backends*)))
    PROVIDE(__stop_log_backends = .);
  } > FLASH
    .nrf_balloc :
  {
    PROVIDE(__start_nrf_balloc = .);
    KEEP(*(.nrf_balloc))
    PROVIDE(__stop_nrf_balloc = .);
  } > FLASH

} INSERT AFTER .text

INCLUDE "nrf_common.ld"
