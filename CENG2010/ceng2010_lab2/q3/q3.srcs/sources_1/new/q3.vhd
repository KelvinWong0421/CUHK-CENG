----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 09/26/2022 06:14:17 PM
-- Design Name: 
-- Module Name: q3 - Behavioral
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

entity q3 is
 Port ( sw : in std_logic_vector(1 downto 0);
        led: out std_logic_vector(1 downto 0));
end q3;

architecture Behavioral of q3 is
signal temp: std_logic_vector(1 downto 0);
begin
    
    led(0) <= sw(0) nand temp(1);
    led(1) <= sw(1) nand temp(0);
    temp(0) <= sw(0) nand temp(1);
    temp(1) <= sw(1) nand temp(0);

end Behavioral;
