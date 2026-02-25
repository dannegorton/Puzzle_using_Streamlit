import streamlit as st
import random

def init_puzzle():
    puzzle = list(range(1, 9)) + [None]
    random.shuffle(puzzle)
    # Ensure the puzzle is solvable
    while not is_solvable(puzzle):
        random.shuffle(puzzle)
    return puzzle

def is_solvable(puzzle):
    # Count inversions
    inversions = 0
    for i in range(len(puzzle)):
        for j in range(i + 1, len(puzzle)):
            if puzzle[i] and puzzle[j] and puzzle[i] > puzzle[j]:
                inversions += 1
    return inversions % 2 == 0

def is_solved(puzzle):
    return puzzle == list(range(1, 9)) + [None]

def find_empty(puzzle):
    return puzzle.index(None)

def move_tile(puzzle, tile):
    empty = find_empty(puzzle)
    tile_index = puzzle.index(tile)
    # Check if the tile is adjacent to the empty space
    if abs(empty - tile_index) in [1, 3]:
        puzzle[empty], puzzle[tile_index] = puzzle[tile_index], puzzle[empty]
    return puzzle

def draw_puzzle(puzzle):
    st.write("### 3x3 Sliding Puzzle")
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            index = i * 3 + j
            if puzzle[index] is not None:
                if cols[j].button(str(puzzle[index]), key=f"btn_{index}"):
                    st.session_state.puzzle = move_tile(st.session_state.puzzle.copy(), puzzle[index])
                    st.rerun()
            else:
                cols[j].button("", disabled=True, key=f"empty_{index}")

def main():
    st.title("Sliding Puzzle Game")
    if "puzzle" not in st.session_state:
        st.session_state.puzzle = init_puzzle()

    draw_puzzle(st.session_state.puzzle)

    if is_solved(st.session_state.puzzle):
        st.success("Congratulations! You solved the puzzle!")
        if st.button("New Game"):
            st.session_state.puzzle = init_puzzle()
            st.rerun()

if __name__ == "__main__":
    main()
