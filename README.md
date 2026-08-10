### Performance and debugging question in python and rust 
Python performance focus right now on: asyncio internals, profiling (cProfile, py-spy), vectorisation in NumPy/Polars, memory, where  the GIL bites

RUST NOTES 
- > cargo rustc -- -Z self-profile
 
 This will generate a breakdown showing exactly how much time the compiler spends in the type_check phase verses the actual code generation phase