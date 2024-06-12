from ui import UI
instance = UI()


def main():
    instance.insert_keys()
    instance.root.mainloop()


if __name__ == "__main__":
    main()
