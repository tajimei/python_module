# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_seed_inventory.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: meitajima <mtajima@student.42tokyo.jp>     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/24 16:48:49 by mtajima           #+#    #+#              #
#    Updated: 2026/05/25 17:46:25 by meitajima        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    name = seed_type.capitalize() 

    if unit == "packets":
        print(f"{name} seeds: {quantity} packets available")
    elif unit == "grams":
        print(f"{name} seeds: {quantity} grams total")
    elif unit == "area":
        print(f"{name} seeds: covers {quantity} square meters")
    else:
        print("Unknown unit type")