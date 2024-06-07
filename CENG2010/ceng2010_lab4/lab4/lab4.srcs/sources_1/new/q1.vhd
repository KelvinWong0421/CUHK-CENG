----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 10/10/2022 04:35:06 PM
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
   Port (sw : in std_logic_vector(0 downto 0);
         btnC,btnD : in std_logic ;
         led: out std_logic_vector(7 downto 0) 
   );
end q1;

architecture Behavioral of q1 is
    type state_type is(
        S0,
        S1,
        S2    
        );
    signal state , next_state: state_type; 
    signal an0: std_logic;
begin
SYNC_PROC : process(btnC,BtnD)
begin
    if BtnD ='1' then
        state <= S0;
        led(0) <= '0';
    else 
        if rising_edge(btnC)then
            state <= next_state;
            led(0) <= an0;
        end if;         
    end if;
end process;

NEXT_STATE_DECODE : process(state,sw(0))
begin
    case (state) is
        when S0 =>
            led(5) <='1';
            led(6) <='0';
            led(7) <='0';
            if sw(0) = '0' then
                next_state <= S0;
            else
                next_state <= S1;
            end if;
        when S1 =>
            led(5) <='0';
            led(6) <='1';
            led(7) <='0';
            if sw(0) = '0' then
                next_state <= S2;
            else
                next_state <= S1;
            end if;
        when S2 =>
            led(5) <='0';
            led(6) <='0';
            led(7) <='1';
            if sw(0) = '0' then
                next_state <= S2;
            else
                next_state <= S1;
            end if; 
        when others =>
            led(5) <='1';
            led(6) <='0';
            led(7) <='0';
            next_state <= S0;                 
    end case;
end process;

OUTPUT_DECODE : process (state, sw(0))
begin
    case (state) is 
        when S0 =>
            if(sw(0)='1') then
                an0 <= '1';
            else
                an0 <= '0';    
            end if;
        when S1 =>
            if(sw(0)='1') then
                an0 <= '1';
            else
                an0 <= '0';     
            end if;
        when S2 =>
            if(sw(0)='1') then
                an0 <= '1';
            else
                an0 <= '0';     
            end if;
        when others =>
            an0 <= '0';
    end case;
end process;                                      
end Behavioral;
