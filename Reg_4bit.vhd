----------------------------------------------------------------------------------
-- Company: 
-- Engineer:  
-- 
-- Create Date:    19:26:13 10/10/2022 
-- Design Name:    4-bit resettable(Asynchronous Register)
-- Module Name:    Reg_4bit - Behavioral 
-- Project Name:  LU Design
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 


-- This module contains the VHDL code that implements the four bit resettable register

------------------------------------------------------------------
-------- A 4-bit register with with an asynchronous reset---------
------------------------------------------------------------------

-- Library dependencies

LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;

-- Entity Declarations(Design)

ENTITY Reg_4bit IS PORT (

    CLK, RES : IN STD_LOGIC; -- Clock and reset
    D_QA : IN STD_LOGIC_VECTOR(3 DOWNTO 0); -- 4-bit input
    Q : OUT STD_LOGIC_VECTOR(3 DOWNTO 0)   -- 4-bit output

);
END ENTITY Reg_4bit;

-- Architecture definition (Models the behaviour or rtl design of the 4-bit regiser)

ARCHITECTURE ASYNC_REG_4BIT_ARCH OF Reg_4bit IS
BEGIN
    REG_4BIT_PROC : PROCESS (CLK, RES) IS -- Asynchronous Reset which occurs immediately once asserted

    BEGIN
        IF RES = '1' THEN -- Once asserted, the output should be 0000
            Q <= "0000";
        ELSIF CLK' EVENT AND CLK = '1' THEN
            Q <= D_QA; -- On the rising edge the output Q, should follow the input D_QA if the reset is not assserted
        END IF;
    END PROCESS REG_4BIT_PROC;

END ASYNC_REG_4BIT_ARCH;