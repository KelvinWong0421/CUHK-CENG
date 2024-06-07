----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/17/2022 08:10:13 PM
-- Design Name: 
-- Module Name: tb - Behavioral
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

entity tb is
--  Port ( );
end tb;

architecture Behavioral of tb is

    component DivideBy2Counter
        Port(
            input: in std_logic;
            output: out std_logic_vector(0 downto 0)
        );
    end component;
    signal ext_input, ext_output: std_logic;
    constant clock_period : time := 100ns;
begin
    utt : DivideBy2Counter
    port map(
        input => ext_input, output(0) => ext_output
    );
    
    clock_process :process 
    begin
        ext_input <= '0'; 
        wait for clock_period/2; 
        ext_input <= '1'; 
        wait for clock_period/2; 
    end process;
    
    stimuli: process
    begin
        wait for 100ns;
        wait for clock_period*10;
        wait;
    end process;


end Behavioral;
