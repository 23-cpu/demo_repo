----------------------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    15:57:30 10/11/2022 
-- Design Name: 
-- Module Name:    Logic_U - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
-----------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------
-------- This module contains the VHDL code for the logic Unit as described in diagram---------
-----------------------------------------------------------------------------------------------

-- Library Declarationss

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
--library UNISIM;
--use UNISIM.VComponents.all;

-- Entity Declaration(Design)

ENTITY Logic_U IS
    PORT (

        A, B : IN signed(3 DOWNTO 0);
        OPCODE : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
        QA : OUT signed(3 DOWNTO 0)

    );
END Logic_U;

-- Architecture Defintion (Models the behaviour or rtl design of the ALU like circuit)

ARCHITECTURE Behavioural OF Logic_U IS
BEGIN
    Behavioural_proc : PROCESS (A, B, OPCODE) IS
    BEGIN
        CASE OPCODE IS
            -- The following gives defines the OPCODES and their logic functions
            WHEN "0000" => QA <= NOT B; -- OPCODE 0000, which translates not B (not gate) 
            WHEN "0001" => QA <= A AND B;
            WHEN "0010" => QA <= A XOR B;
            WHEN "0011" => QA <= B;
            WHEN "0100" => QA <= NOT(A XOR B);
            WHEN "0101" => QA <= (A AND "0001");
            WHEN "0110" => QA <= NOT(B AND "1010");
            WHEN "0111" => QA <= NOT(B OR "1010");
            WHEN "1000" => QA <= NOT A;
            WHEN "1001" => QA <= NOT(A OR "0101");
            WHEN "1010" => QA <= A XNOR B;

            WHEN OTHERS =>
                NULL;
        END CASE;

    END PROCESS Behavioural_proc;

END Behavioural;