import * as Dialog from "@radix-ui/react-dialog";

export function AssuranceDialog() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <button className="button button--secondary" type="button">
          Review assurance details
        </button>
      </Dialog.Trigger>
      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content">
          <Dialog.Title>What PortAtlas can assure</Dialog.Title>
          <Dialog.Description>
            Registry coordination and operating-system ownership are different
            boundaries.
          </Dialog.Description>
          <div className="dialog-copy">
            <p>
              A reservation or atomic lease coordinates cooperating PortAtlas clients.
              It does not bind an operating-system socket.
            </p>
            <p>
              An unmanaged process can ignore the registry or take a port after a
              point-in-time check. Recheck runtime evidence when the process starts.
            </p>
            <p>
              Source patching, managed launch, and process termination are not available
              in the MVP.
            </p>
          </div>
          <Dialog.Close asChild>
            <button className="button" type="button">
              Close details
            </button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
