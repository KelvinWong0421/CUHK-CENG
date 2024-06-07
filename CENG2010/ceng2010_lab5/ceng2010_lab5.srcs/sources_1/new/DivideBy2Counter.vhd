----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/17/2022 05:53:55 PM
-- Design Name: 
-- Module Name: DivideBy2Counter - Behavioral
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

entity DivideBy2Counter is
  Port (input:in std_logic;
  output:out std_logic_vector(0 downto 0));
end DivideBy2Counter;

architecture Behavioral of DivideBy2Counter is
    component q2
        Port (sw: in std_logic_vector(0 downto 0);
        btnC: in std_logic;
        led: out std_logic_vector(1 downto 0) );
    end component; 
    signal nq : std_logic:='0';  
begin
    D2c: q2 port map(
    sw(0) => nq, btnC => input,
    led(0) => output(0),led(1) => nq
    );

end Behavioral;
