----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/17/2022 04:54:17 PM
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
  Port (sw: in std_logic_vector(0 downto 0);
        btnC: in std_logic;
        led: out std_logic_vector(1 downto 0) );
end q2;

architecture Behavioral of q2 is
    signal q, qp : std_logic := '0';    
begin
        led(0) <= q;
        led(1) <= qp;
process (sw,btnC)
begin
    if (rising_edge(btnC)) then
        q <= sw(0);
        qp <= not sw(0); 

    end if;    
end process;

end Behavioral;
