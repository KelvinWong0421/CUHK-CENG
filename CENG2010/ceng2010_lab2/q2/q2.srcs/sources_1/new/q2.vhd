----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 09/26/2022 05:17:34 PM
-- Design Name: 
-- Module Name: q2 - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity q2 is
      Port (sw: in std_logic_vector(3 downto 0);
            seg: out std_logic_vector(6 downto 0);
            an: out std_logic_vector(3 downto 0));
      
end q2;

architecture Behavioral of q2 is

begin
an(0) <= '0';
an(1) <= '1';
an(2) <= '1';
an(3) <= '1';

with sw select
--------GFEDCBA--------
seg <= "1111001" when "0001", 
       "0100100" when "0010",     
       "0110000" when "0011",
       "0011001" when "0100", 
       "0010010" when "0101", 
       "0000010" when "0110", 
       "1111000" when "0111", 
       "0000000" when "1000", 
       "0010000" when "1001",
       "0000110" when others;
end Behavioral;
