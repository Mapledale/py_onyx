def func(a, **kwargs):
    ax2 = a * a
    print(f'a: {ax2}')

    print(kwargs)
    if 'amp' in kwargs:
        b = kwargs['b']
        print(f'b: {b}, amp is {kwargs["amp"]}')


def main():
    print('try 1:')
    func(5)

    print('try 2:')
    func(5, amp=True, b=6)


if __name__ == '__main__':
    main()
