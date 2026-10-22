import sys
from main import main


try:
    main()

except KeyboardInterrupt:
    print("\n[!] Process interrupted by user. Exiting...")
    sys.exit(0)
