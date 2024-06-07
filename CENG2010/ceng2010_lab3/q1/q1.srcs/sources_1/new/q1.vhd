----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/03/2022 04:28:45 PM
-- Design Name: 
-- Module Name: q1 - Behavioral
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

entity q1 is
   Port ( 
   sw: in std_logic_vector(6 downto 0);
   seg: out std_logic_vector(6 downto 0);
   an: out std_logic_vector(3 downto 0); 
   btnC: in std_logic      
   );
end q1;

architecture Behavioral of q1 is
signal a : std_logic_vector(3 downto 0):="0011"; 

begin
    
    an <= a;


    process(btnC,a)
        begin 
        if  rising_edge(btnC) then
            if (a = "0011") then
             a <= "1100";
            else
             a <= "0011";
            end if;
        end if;
    end process; 




seg(0) <= not sw(0);
seg(1) <= not sw(1);
seg(2) <= not sw(2);
seg(3) <= not sw(3);
seg(4) <= not sw(4);
seg(5) <= not sw(5);
seg(6) <= not sw(6);

          

end Behavioral;
