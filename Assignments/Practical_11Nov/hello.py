from mpi4py import MPI
communicator = MPI.COMM_WORLD
rank = communicator.rank
print("hello")