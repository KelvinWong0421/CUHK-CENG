----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/04/2022 11:04:17 AM
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
Port (
 sw :in  std_logic_vector(3 downto 0);
 btnC: in std_logic :='1';
 led: out std_logic_vector(1 downto 0)
 );
end q2;

architecture Behavioral of q2 is
signal a: std_logic_vector(1 downto 0);
begin

led <= a;

process(btnC,sw,a)
begin
    if(sw(3) ='0') and (sw(2) ='1') then 
        a <= "10";
    elsif (sw(3) ='1') and (sw(2) ='0') then  
        a <= "01";
    elsif (sw(3) ='0') and (sw(2) ='0') then 
        a <= "11";
    elsif (sw(3) ='1') and (sw(2) ='1') then
        
      if falling_edge(btnC) then
        if (sw(1) ='0') and (sw(0) ='0')  then
            a <= a;
        elsif (sw(1) ='0') and (sw(0) ='1') then
            a <= "01";
        elsif (sw(1) ='1') and (sw(0) ='0') then
            a <= "10";
        elsif (sw(1) ='1') and (sw(0) ='1') then
            a <= not(a);                  
        else  
            a <= a;
        end if;
       end if;    
   end if; 

end process;


end Behavioral;
