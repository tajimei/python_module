# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_count_harvest_recursive.py                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: meitajima <mtajima@student.42tokyo.jp>     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/24 16:48:31 by mtajima           #+#    #+#              #
#    Updated: 2026/05/25 13:42:51 by meitajima        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))
    def count(i):
        if i > days:
            return
        print(f"Day {i}")
        count(i + 1)
    count(1) 
    print("Harvest time!")

    # count(1) で定義したcount関数を引数１で呼び出す